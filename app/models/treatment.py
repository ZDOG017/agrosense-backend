from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, Numeric, String, text
from sqlalchemy.orm import relationship

from app.database import Base


class Treatment(Base):
    __tablename__ = "treatments"
    __table_args__ = (
        CheckConstraint(
            "treatment_type IN ('Fertilizer', 'Pesticide', 'Soil Improvement', 'Disease Control')",
            name="ck_treatments_type",
        ),
        CheckConstraint("quantity >= 0", name="ck_treatments_quantity_non_negative"),
        CheckConstraint("cost >= 0", name="ck_treatments_cost_non_negative"),
    )

    treatment_id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.field_id", ondelete="CASCADE"), nullable=False)
    crop_id = Column(Integer, ForeignKey("crops.crop_id", ondelete="SET NULL"))
    treatment_type = Column(String(50), nullable=False)
    material_used = Column(String(100))
    quantity = Column(Numeric(10, 2))
    unit = Column(String(20))
    treatment_date = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    cost = Column(Numeric(10, 2), nullable=False, default=0, server_default="0")
    responsible_user_id = Column(Integer, ForeignKey("users.user_id"))

    field = relationship("Field", back_populates="treatments")
    crop = relationship("Crop", back_populates="treatments")
    responsible_user = relationship("User", back_populates="treatments")
