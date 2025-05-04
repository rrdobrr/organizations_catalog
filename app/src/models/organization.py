from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime, func
from sqlalchemy.orm import relationship

from app.src.core.db.base import Base


organization_activity_association = Table(
    "organizations_activity",
    Base.metadata,
    Column(
        "organization_id", Integer, ForeignKey("organizations.id"), primary_key=True
    ),
    Column(
        "activity_type_id", Integer, ForeignKey("activity_types.id"), primary_key=True
    ),
)


class Phone(Base):
    __tablename__ = "phones"
    id = Column(Integer, primary_key=True)
    number = Column(String(50), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("Organization", back_populates="phones")


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    building = relationship("Building", back_populates="organizations")
    activity_types = relationship(
        "ActivityTypes",
        secondary=organization_activity_association,
        back_populates="organizations",
    )
    phones = relationship(
        "Phone",
        back_populates="organization",
        cascade="all, delete-orphan",
        lazy="selectin"  # 👈 обязательно!
    )

