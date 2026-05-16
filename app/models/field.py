from sqlalchemy import CheckConstraint, Column, DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class Field(Base):
    __tablename__ = "fields"
    __table_args__ = (
        CheckConstraint("area_hectares > 0", name="ck_fields_area_positive"),
        CheckConstraint(
            "status IN ('Healthy', 'Needs Irrigation', 'Under Treatment', 'Ready for Harvest')",
            name="ck_fields_status",
        ),
    )

    field_id = Column(Integer, primary_key=True, index=True)
    field_name = Column(String(100), nullable=False)
    location = Column(String(100))
    area_hectares = Column(Numeric(10, 2), nullable=False)
    soil_type = Column(String(50))
    status = Column(String(50), nullable=False, default="Healthy", server_default="Healthy")
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    crops = relationship("Crop", back_populates="field", cascade="all, delete-orphan")
    sensors = relationship("Sensor", back_populates="field", cascade="all, delete-orphan")
    irrigation_schedules = relationship(
        "IrrigationSchedule",
        back_populates="field",
        cascade="all, delete-orphan",
    )
    tasks = relationship("Task", back_populates="field")
    treatments = relationship("Treatment", back_populates="field", cascade="all, delete-orphan")
    harvest_records = relationship(
        "HarvestRecord",
        back_populates="field",
        cascade="all, delete-orphan",
    )
