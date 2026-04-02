from fastapi import FastAPI

app = FastAPI(
    title="Yomitan Platform API",
    description="Backend for the Yomitan-powered Japanese learning SPA.",
    version="1.0.0"
)

@app.get("/health", tags=["Health"])
def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}