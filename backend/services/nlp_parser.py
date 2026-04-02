# backend/services/nlp_parser.py
import fugashi

# Initialize the tagger once globally so we don't reload the dictionary on every single request
tagger = fugashi.Tagger()

def parse_japanese_text(text: str) -> list[dict]:
    """
    Takes a raw Japanese string and returns a list of token dictionaries
    containing the surface form, base dictionary form, and part of speech.
    """
    parsed_tokens = []
    
    # tagger(text) returns an iterator of UnidicNode objects
    for word in tagger(text):
        # Unidic-lite features are heavily detailed. We extract the essentials.
        # feature.lemma is the dictionary form. If it's missing, fallback to the surface form.
        base_form = word.feature.lemma if word.feature.lemma else word.surface
        
        parsed_tokens.append({
            "surface": word.surface,
            "base_form": base_form,
            "pos": word.feature.pos1  # Main Part of Speech (e.g., Noun, Verb, Particle)
        })
        
    return parsed_tokens

