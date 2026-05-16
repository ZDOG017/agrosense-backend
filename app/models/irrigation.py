from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class IrrigationSchedule(Base):
    __tablename__ = "irrigation_schedules"
    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="ck_irrigation_duration_positive"),
        CheckConstraint("water_amount_liters > 0", name="ck_irrigation_water_positive"),
        CheckConstraint("mode IN ('Manual', 'Automatic')", name="ck_irrigation_mode"),
        CheckConstraint(
            "status IN ('Scheduled', 'Completed', 'Cancelled')",
            name="ck_irrigation_status",
        ),
    )

    irrigation_id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.field_id", ondelete="CASCADE"), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    water_amount_liters = Column(Numeric(10, 2), nullable=False)
    mode = Column(String(20), nullable=False, default="Manual", server_default="Manual")
    status = Column(
        String(20),
        nullable=False,
        default="Scheduled",
        server_default="Scheduled",
    )
    created_by = Column(Integer, ForeignKey("users.user_id"))

    field = relationship("Field", back_populates="irrigation_schedules")
    creator = relationship("User", back_populates="irrigation_schedules")
