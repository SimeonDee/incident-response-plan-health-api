from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    # MySQL requires VARCHAR lengths.
    incident_type = Column(String(100), index=True)
    description = Column(String(1000))
    location = Column(String(255))
    date_time = Column(DateTime)
    severity_level = Column(String(50))
    contact_information = Column(String(150), unique=True, nullable=True)
