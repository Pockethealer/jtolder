# backend/services/dictionary_importer.py
import zipfile
import json
import os
from sqlalchemy.orm import Session
from core.database import SessionLocal  # Need this to create a new session in the background
from models.dictionary import Dictionary
from models.term import DictionaryTerm

# We pass the file path instead of bytes, and create our own DB session 
# because this runs in the background after the HTTP request is closed.
def process_dictionary_background(file_path: str, task_id: str):
    db = SessionLocal()
    try:
        with zipfile.ZipFile(file_path) as archive:
            # 1. Parse index.json
            with archive.open("index.json") as f:
                index_data = json.load(f)
                
            new_dict = Dictionary(
                title=index_data.get("title", "Unknown Dictionary"),
                revision=index_data.get("revision", ""),
                is_sequenced=index_data.get("sequenced", False),
                format=index_data.get("format", 3)
            )
            db.add(new_dict)
            db.commit()
            db.refresh(new_dict) 
            
            # 2. Parse bank files (same logic as before)
            bank_files = [n for n in archive.namelist() if "bank_" in n and n.endswith(".json")]
            terms_to_insert = []
            
            for bank_file in bank_files:
                if "tag_bank" in bank_file: continue 
                    
                with archive.open(bank_file) as f:
                    bank_data = json.load(f)
                    for entry in bank_data:
                        term_string = entry[0]
                        reading_string = entry[1] if isinstance(entry[1], str) and entry[1] else None
                        sequence_val = entry[6] if len(entry) > 6 and isinstance(entry[6], int) else 0

                        terms_to_insert.append(
                            DictionaryTerm(
                                dictionary_id=new_dict.id,
                                term=term_string,
                                reading=reading_string,
                                sequence=sequence_val,
                                definition_data=entry 
                            )
                        )
                        if len(terms_to_insert) >= 10000:
                            db.add_all(terms_to_insert)
                            db.commit()
                            terms_to_insert = []
            
            if terms_to_insert:
                db.add_all(terms_to_insert)
                db.commit()
                
        # Update our global status dictionary (see main.py)
        from main import import_statuses
        import_statuses[task_id] = {"status": "completed", "title": new_dict.title}
        
    except Exception as e:
        from main import import_statuses
        import_statuses[task_id] = {"status": "failed", "error": str(e)}
    finally:
        db.close()
        # Clean up the temp file!
        if os.path.exists(file_path):
            os.remove(file_path)