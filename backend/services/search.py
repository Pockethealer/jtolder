# backend/services/search.py
import json
import logging
import os
import re
from sqlalchemy.orm import Session
from models.term import DictionaryTerm
import unicodedata
from sqlalchemy import or_

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_PATH = os.path.join(BASE_DIR, './deinflect_rules.json')

with open(RULES_PATH, 'r', encoding='utf-8') as f:
    DEINFLECT_RULES = json.load(f)

# Maximum deinflection chain depth.
# Set to 5 to handle complex conjugation chains like:
#   食べさせられなかった → 食べさせられない → 食べさせられる → 食べさせる → 食べる
MAX_DEINFLECT_DEPTH = 5

# ---------------------------------------------------------
# 1. TEXT PREPROCESSOR
# ---------------------------------------------------------
def preprocess_japanese_text(text: str) -> list[str]:
    """
    Returns a list of variations (Original, Normalised, and Fully Collapsed).
    """
    # 1. Basic Normalization (Half-width to Full-width, etc.)
    base = unicodedata.normalize('NFKC', text)
    variations = {base}
    
    # 2. Partial Collapse (3+ -> 2)
    partial = re.sub(r'[っッ]{3,}', 'っっ', base)
    partial = re.sub(r'ー{2,}', 'ー', partial)
    variations.add(partial)
    
    # 3. Full Collapse (Slang removal: すっごーい -> すごい)
    # This allows us to match the dictionary headword directly
    full = re.sub(r'[っッ]+', '', base) # Remove all small tsu
    full = re.sub(r'ー+', '', full)     # Remove all long vowels
    variations.add(full)
    
    return list(variations)

# ---------------------------------------------------------
# 2. RECURSIVE DE-INFLECTOR / PREFIX GENERATOR
# ---------------------------------------------------------
def generate_search_terms(raw_string: str) -> dict:
    """
    For every prefix of raw_string, recursively apply deinflection rules and
    collect candidate dictionary headwords together with metadata needed for
    POS validation and match-length scoring.

    Return value — search_map:
        {
            candidate_headword: [
                {
                    "source_len":    int,        # characters of raw_string consumed
                    "conditions_in": set[str],   # POS tags the DB entry must satisfy
                                                 # (empty set = unconditionally valid)
                },
                ...
            ],
            ...
        }

    Rule schema (conditions_in / conditions_out):
        conditions_in  – tags that the CURRENT inflected form must already
                         satisfy before this rule may fire.  Empty list means
                         the rule fires unconditionally.
        conditions_out – tags propagated to the next rule in the chain, AND
                         used as the final POS filter when no further rules
                         fire (i.e. they describe what the resulting base form
                         is expected to be in the dictionary).
    """
    search_map: dict[str, list[dict]] = {}

    def record(text: str, source_len: int, conditions_in: frozenset) -> None:
        """Store a (text, source_len, conditions_in) tuple, deduplicating."""
        entry = {"source_len": source_len, "conditions_in": conditions_in}
        if text not in search_map:
            search_map[text] = []
        # Avoid exact duplicates that arise from multiple rule paths
        if entry not in search_map[text]:
            search_map[text].append(entry)

    def apply_rules(
        text: str,
        source_len: int,
        active_conditions: frozenset,
        depth: int,
    ) -> None:
        """
        Recursively deinflect `text`.

        active_conditions:
            The conditions_out emitted by the rule that produced `text`.
            They act as conditions_in guards for the *next* rule application,
            AND as the final dictionary POS filter if no further rules fire.
        """
        # Always record this form as a candidate headword.
        # active_conditions become the conditions_in that the DB entry must match.
        record(text, source_len, active_conditions)

        if depth >= MAX_DEINFLECT_DEPTH:
            return

        for suffix, rule_list in DEINFLECT_RULES.items():
            if not text.endswith(suffix):
                continue

            for rule in rule_list:
                rule_conditions_in  = frozenset(rule.get("conditions_in",  []))
                rule_conditions_out = frozenset(rule.get("conditions_out", []))

                # Gate: if the rule requires specific incoming conditions,
                # the current active_conditions must satisfy at least one.
                # An empty conditions_in means the rule fires unconditionally.
                if rule_conditions_in and active_conditions and not rule_conditions_in.intersection(active_conditions):
                    if depth > 0:
                        continue

                base_form = text[: -len(suffix)] + rule["replacement"]

                # Propagate conditions_out as the new active_conditions for the
                # next level.  These REPLACE (not accumulate) the current ones
                # because each rule fully describes the resulting form's grammar.
                apply_rules(base_form, source_len, rule_conditions_out, depth + 1)

    for i in range(len(raw_string), 0, -1):
        prefix = raw_string[:i]
        # Start each prefix chain with an empty active_conditions set so the
        # first rule is always tried unconditionally.
        apply_rules(prefix, len(prefix), frozenset(), 0)

    return search_map


# ---------------------------------------------------------
# 3. DATABASE SEARCH & POS VALIDATION
# ---------------------------------------------------------
def _extract_dict_tags(row: DictionaryTerm) -> frozenset:
    """
    Safely extract the POS tag string from a Yomitan term-bank row.

    Yomitan term bank v3 layout:
        [term, reading, definition_tags, rules, score, definitions, ...]
    Index 2 is the definition/POS tags string.
    """
    tags = set()
    try:
        data = row.definition_data
        
        # Extract display tags
        if len(data) > 2 and isinstance(data[2], str):
            tags.update(data[2].split())
            
        # Extract rule tags (This is where 'adj-i' and 'v1' actually live!)
        if len(data) > 3 and isinstance(data[3], str):
            tags.update(data[3].split())
            
        return frozenset(tags)
    except Exception:
        logger.warning("Failed to extract tags for term %r", row.term, exc_info=True)
        return frozenset()

def _extract_score(row: DictionaryTerm) -> int:
    """
    Safely extract the frequency/priority score from Index 4 of the Yomitan array.
    Higher scores should be ranked higher in the UI.
    """
    try:
        if len(row.definition_data) > 4:
            score = row.definition_data[4]
            if isinstance(score, (int, float)):
                return int(score)
    except Exception:
        pass
    return 0

def search_dictionary(db: Session, raw_text: str) -> list:
    clean_variations = preprocess_japanese_text(raw_text)
    
    # 2. Generate search terms for EVERY variation
    combined_search_map = {}
    for variation in clean_variations:
        variant_map = generate_search_terms(variation)
        # Merge results into the main map
        for term, paths in variant_map.items():
            if term not in combined_search_map:
                combined_search_map[term] = []
            combined_search_map[term].extend(paths)

    search_terms = list(combined_search_map.keys())
    # 2. Bulk query — search BOTH the term and the reading!
    raw_results = db.query(DictionaryTerm).filter(
        or_(
            DictionaryTerm.term.in_(search_terms),
            DictionaryTerm.reading.in_(search_terms)
        )
    ).all()

    valid_results = []

    # 3. POS validation and longest-match selection
    for row in raw_results:
        dict_tags = _extract_dict_tags(row)
        
        # Look up paths using the term...
        paths = combined_search_map.get(row.term, [])
        
        # AND look up paths using the reading! (Crucial for words like 明日/あした)
        if row.reading and row.reading in combined_search_map:
            # We convert it to a new list so we don't accidentally mutate the original dictionary
            paths = paths + combined_search_map[row.reading] 

        best_source_len = -1

        for path in paths:
            conditions_in = path["conditions_in"]

            # A path is valid when:
            #   a) No POS conditions are required
            #   b) The dictionary provides NO tags
            #   c) At least one required condition is present
            if not conditions_in or not dict_tags or conditions_in.intersection(dict_tags):
                if path["source_len"] > best_source_len:
                    best_source_len = path["source_len"]

        if best_source_len > -1:
            row.match_len = best_source_len
            valid_results.append(row)

    # 4. Sort by how much of the original input was consumed
    valid_results.sort(
        key=lambda r: (getattr(r, "match_len", 0), _extract_score(r)), 
        reverse=True
    )
    return valid_results