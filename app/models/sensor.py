from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

from app.database import Base


class Sensor(Base):
    __tablename__ = "sensors"
    __table_args__ = (
        CheckConstraint(
            "sensor_type IN ('Soil Moisture', 'Temperature', 'Humidity', 'pH', 'Light', 'Water Level')",
            name="ck_sensors_type",
        ),
        CheckConstraint(
            "status IN ('Online', 'Offline', 'Maintenance')",
            name="ck_sensors_status",
        ),
    )

    sensor_id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.field_id", ondelete="CASCADE"), nullable=False)
    sensor_type = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False, default="Online", server_default="Online")
    installed_date = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))

    field = relationship("Field", back_populates="sensors")
    readings = relationship("SensorReading", back_populates="sensor", cascade="all, delete-orphan")
