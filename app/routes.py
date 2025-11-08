from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.models import Incident
from app.database import get_db
from app.schemas import IncidentCreate, IncidentUpdate, IncidentResponse

router = APIRouter()


@router.post("/incidents/", response_model=IncidentResponse)
def create_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    db_incident = Incident(
        incident_type=incident.incident_type,
        description=incident.description,
        location=incident.location,
        date_time=incident.date_time,
        severity_level=incident.severity_level,
        contact_information=incident.contact_information,
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident


@router.get("/incidents/", response_model=List[IncidentResponse])
def list_incidents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    incidents = db.query(Incident).offset(skip).limit(limit).all()
    return incidents


@router.get("/incidents/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.put("/incidents/{incident_id}", response_model=IncidentResponse)
def update_incident(
    incident_id: int, incident: IncidentUpdate, db: Session = Depends(get_db)
):
    db_incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if db_incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    for var, value in vars(incident).items():
        if value is not None:
            setattr(db_incident, var, value)

    db.commit()
    db.refresh(db_incident)
    return db_incident


@router.delete("/incidents/{incident_id}")
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    db.delete(incident)
    db.commit()
    return {"message": "Incident deleted successfully"}
