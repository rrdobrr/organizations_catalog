from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from app.src.core.db.base import Base
from .organization import organization_activity_association


class ActivityTypes(Base):
    __tablename__ = "activity_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(
        String(255), nullable=False, unique=True, comment="Название типа активности"
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    parent_id = Column(Integer, ForeignKey("activity_types.id", ondelete="SET NULL"))
    organizations = relationship(
        "Organization",
        secondary=organization_activity_association,
        back_populates="activity_types",
    )
