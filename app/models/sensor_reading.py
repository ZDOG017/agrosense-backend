from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from app.database import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"
    __table_args__ = (
        CheckConstraint(
            "alert_level IN ('Normal', 'Warning', 'Critical')",
            name="ck_sensor_readings_alert_level",
        ),
    )

    reading_id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.sensor_id", ondelete="CASCADE"), nullable=False)
    reading_value = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(20), nullable=False)
    reading_time = Column(DateTime, nullable=False, server_default=func.current_timestamp())
    alert_level = Column(
        String(20),
        nullable=False,
        default="Normal",
        server_default="Normal",
    )

    sensor = relationship("Sensor", back_populates="readings")
