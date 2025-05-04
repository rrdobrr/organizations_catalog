from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from geoalchemy2.types import Geography
from geoalchemy2.functions import ST_SetSRID, ST_MakePoint

from app.src.core.db.base import Base


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location = Column(Geography(geometry_type="POINT", srid=4326))

    def __repr__(self):
        return f"<Building(id={self.id}, name={self.name}, latitude={self.latitude}, longitude={self.longitude})>"

    def set_location(self):
        self.location = ST_SetSRID(ST_MakePoint(self.longitude, self.latitude), 4326)

    organizations = relationship("Organization", back_populates="building")
