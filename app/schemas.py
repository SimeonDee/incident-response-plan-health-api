from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class IncidentBase(BaseModel):
    incident_type: str
    description: str
    location: str
    date_time: datetime
    severity_level: str
    contact_information: Optional[str] = None


class IncidentCreate(IncidentBase):
    pass


class IncidentUpdate(BaseModel):
    incident_type: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    date_time: Optional[datetime] = None
    severity_level: Optional[str] = None
    contact_information: Optional[str] = None


class IncidentResponse(IncidentBase):
    id: int

    class Config:
        from_attributes = True  # This replaces orm_mode in Pydantic v2
