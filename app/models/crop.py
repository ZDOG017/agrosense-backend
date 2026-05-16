from sqlalchemy import CheckConstraint, Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class Crop(Base):
    __tablename__ = "crops"
    __table_args__ = (
        CheckConstraint(
            "growth_stage IN ('Seedling', 'Vegetative', 'Flowering', 'Fruiting', 'Harvest Ready')",
            name="ck_crops_growth_stage",
        ),
        CheckConstraint(
            "status IN ('Active', 'Harvested', 'Failed')",
            name="ck_crops_status",
        ),
    )

    crop_id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.field_id", ondelete="CASCADE"), nullable=False)
    crop_name = Column(String(100), nullable=False)
    planting_date = Column(Date, nullable=False)
    expected_harvest_date = Column(Date)
    growth_stage = Column(
        String(50),
        nullable=False,
        default="Seedling",
        server_default="Seedling",
    )
    water_requirement_mm = Column(Numeric(10, 2))
    status = Column(String(30), nullable=False, default="Active", server_default="Active")

    field = relationship("Field", back_populates="crops")
    treatments = relationship("Treatment", back_populates="crop")
    harvest_records = relationship("HarvestRecord", back_populates="crop")
