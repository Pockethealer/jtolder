from fastapi import FastAPI
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