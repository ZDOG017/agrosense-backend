from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("status IN ('Active', 'Inactive')", name="ck_users_status"),
    )

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(Text, nullable=False)
    role_id = Column(Integer, ForeignKey("roles.role_id"), nullable=False)
    status = Column(String(20), nullable=False, default="Active", server_default="Active")
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    role = relationship("Role", back_populates="users")
    irrigation_schedules = relationship("IrrigationSchedule", back_populates="creator")
    tasks = relationship("Task", back_populates="assignee")
    treatments = relationship("Treatment", back_populates="responsible_user")
