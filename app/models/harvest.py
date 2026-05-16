from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, Numeric, String, text
from sqlalchemy.orm import relationship

from app.database import Base


class HarvestRecord(Base):
    __tablename__ = "harvest_records"
    __table_args__ = (
        CheckConstraint("quantity_kg > 0", name="ck_harvest_quantity_positive"),
        CheckConstraint("price_per_kg >= 0", name="ck_harvest_price_non_negative"),
        CheckConstraint("quality_grade IN ('A', 'B', 'C')", name="ck_harvest_quality_grade"),
    )

    harvest_id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.crop_id", ondelete="CASCADE"), nullable=False)
    field_id = Column(Integer, ForeignKey("fields.field_id", ondelete="CASCADE"), nullable=False)
    harvest_date = Column(Date, nullable=False, server_default=text("CURRENT_DATE"))
    quantity_kg = Column(Numeric(10, 2), nullable=False)
    quality_grade = Column(String(10))
    price_per_kg = Column(Numeric(10, 2), nullable=False)
    revenue = Column(Numeric(12, 2))

    crop = relationship("Crop", back_populates="harvest_records")
    field = relationship("Field", back_populates="harvest_records")
