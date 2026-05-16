from sqlalchemy import CheckConstraint, Column, Date, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from app.database import Base


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint("priority IN ('Low', 'Medium', 'High')", name="ck_tasks_priority"),
        CheckConstraint(
            "status IN ('Pending', 'In Progress', 'Completed', 'Cancelled')",
            name="ck_tasks_status",
        ),
    )

    task_id = Column(Integer, primary_key=True, index=True)
    assigned_to = Column(Integer, ForeignKey("users.user_id"))
    field_id = Column(Integer, ForeignKey("fields.field_id", ondelete="SET NULL"))
    task_title = Column(String(150), nullable=False)
    description = Column(Text)
    priority = Column(String(20), nullable=False, default="Medium", server_default="Medium")
    status = Column(String(20), nullable=False, default="Pending", server_default="Pending")
    due_date = Column(Date)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp())

    assignee = relationship("User", back_populates="tasks")
    field = relationship("Field", back_populates="tasks")
