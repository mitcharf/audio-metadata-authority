from fastapi import FastAPI

app = FastAPI(
    title="Metadata Authority & Library Normalization System",
    description="API for the Audio Metadata Authority backend.",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"status": "ok", "detail": "Metadata Authority backend is running."}
