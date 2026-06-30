"""Digital Public Safety Platform — API Gateway."""

from fastapi import FastAPI

app = FastAPI(
    title="Digital Public Safety Platform",
    version="0.1.0",
)


@app.get("/health")
async def health():
    return {"status": "ok"}
