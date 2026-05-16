from fastapi import FastAPI


app = FastAPI(
    title="AgroSense Smart Farming API",
    description="Backend API for the AgroSense Smart Farming Database Management System.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "message": "AgroSense backend is running"}
