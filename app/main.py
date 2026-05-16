from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, engine
from app.models import crop, field, harvest, irrigation, role, sensor, sensor_reading, task, treatment, user  # noqa: F401
from app.routes.auth_routes import router as auth_router
from app.routes.crop_routes import router as crop_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.field_routes import router as field_router
from app.routes.harvest_routes import router as harvest_router
from app.routes.irrigation_routes import router as irrigation_router
from app.routes.report_routes import router as report_router
from app.routes.role_routes import router as role_router
from app.routes.sensor_reading_routes import router as sensor_reading_router
from app.routes.sensor_routes import router as sensor_router
from app.routes.task_routes import router as task_router
from app.routes.treatment_routes import router as treatment_router
from app.routes.user_routes import router as user_router


settings = get_settings()
app = FastAPI(
    title="AgroSense Smart Farming API",
    description="Backend API for the AgroSense Smart Farming Database Management System.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "message": "AgroSense backend is running"}


app.include_router(auth_router)
app.include_router(role_router)
app.include_router(user_router)
app.include_router(field_router)
app.include_router(crop_router)
app.include_router(sensor_router)
app.include_router(sensor_reading_router)
app.include_router(irrigation_router)
app.include_router(task_router)
app.include_router(treatment_router)
app.include_router(harvest_router)
app.include_router(dashboard_router)
app.include_router(report_router)
