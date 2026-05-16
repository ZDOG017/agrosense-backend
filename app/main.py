from fastapi import FastAPI

from app.routes.auth_routes import router as auth_router
from app.routes.crop_routes import router as crop_router
from app.routes.field_routes import router as field_router
from app.routes.role_routes import router as role_router
from app.routes.user_routes import router as user_router


app = FastAPI(
    title="AgroSense Smart Farming API",
    description="Backend API for the AgroSense Smart Farming Database Management System.",
    version="0.7.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "message": "AgroSense backend is running"}


app.include_router(auth_router)
app.include_router(role_router)
app.include_router(user_router)
app.include_router(field_router)
app.include_router(crop_router)
