import shutil
import uuid
import tempfile
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from services.search import search_dictionary
from core.database import get_db
from pydantic import BaseModel, Field
from services.nlp_parser import parse_japanese_text
app = FastAPI(
    title="Yomitan Platform API",
    description="Backend for the Yomitan-powered Japanese learning SPA.",
    version="1.0.0"
)

class ParseRequest(BaseModel):
    text: str = Field(
        ..., 
        max_length=50000, 
        description="The Japanese text to parse. Limited to 5000 characters to prevent DoS."
    )

class SearchRequest(BaseModel):
    # The raw string grabbed by the frontend cursor
    text: str = Field(..., max_length=30)


@app.get("/health", tags=["Health"])
def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}

@app.post("/api/parse", tags=["NLP Engine"])
def parse_text(request: ParseRequest):
    """
    Takes raw Japanese text and returns an array of parsed tokens 
    with their dictionary forms and parts of speech.
    """
    tokens = parse_japanese_text(request.text)
    return {"tokens": tokens}

from services.dictionary_importer import process_dictionary_background

# A simple in-memory dictionary to track task status. 
# (In a massive app, you'd use Redis or a DB table for this, but this is perfect for the MVP).
import_statuses = {}

@app.post("/api/dictionaries/import", tags=["Dictionaries"])
async def upload_dictionary(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Receives the .zip, saves it to a temp file, and starts background processing.
    """
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="File must be a .zip archive")
        
    # Generate a unique ID for this job
    task_id = str(uuid.uuid4())
    import_statuses[task_id] = {"status": "processing"}
    
    # Save the uploaded file to a temporary location safely
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")
    try:
        with temp_file as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
        
    # Hand the file path and task ID off to the background task
    background_tasks.add_task(process_dictionary_background, temp_file.name, task_id)
    
    # Return immediately! The user isn't kept waiting.
    return {
        "message": "File uploaded successfully. Processing started.",
        "task_id": task_id
    }

@app.get("/api/dictionaries/status/{task_id}", tags=["Dictionaries"])
def get_import_status(task_id: str):
    """
    The frontend calls this every 2 seconds to check if the import is done.
    """
    status_data = import_statuses.get(task_id)
    if not status_data:
        raise HTTPException(status_code=404, detail="Task not found")
        
    return status_data

@app.post("/api/dictionary/search", tags=["Dictionaries"])
def lookup_word(request: SearchRequest, db: Session = Depends(get_db)):
    """
    Takes a string from the user's cursor, generates prefixes, 
    de-inflects them, and returns matching dictionary definitions.
    """
    results = search_dictionary(db, request.text)
    
    # Format the data for the frontend
    formatted_results = []
    for r in results:
        formatted_results.append({
            "id": r.id,
            "dictionary_id": r.dictionary_id,
            "term": r.term,
            "reading": r.reading,
            "sequence": r.sequence,
            "data": r.definition_data  # The raw Yomitan JSON blob!
        })
        
    return {"results": formatted_results}


# ----------------------------------SPA-------------------------------------#
STATIC_DIR = "static"


# Mount the /assets folder so the browser can load the CSS and JS
app.mount("/assets", StaticFiles(directory=f"{STATIC_DIR}/assets"), name="assets")
# Catch-all route: Route any unmatched URLs to the React index.html
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    # Prevent the catch-all from swallowing API 404s
    if full_path.startswith("api/"):
        return {"error": "API endpoint not found"}
        
    return FileResponse(f"{STATIC_DIR}/index.html")
