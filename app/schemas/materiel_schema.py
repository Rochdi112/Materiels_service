from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MaterielCreate(BaseModel):
    nom: str
    reference: Optional[str] = None
    date_installation: Optional[datetime] = None
    statut: Optional[str] = "actif"
    site_id: Optional[int] = None

class MaterielRead(BaseModel):
    id: int
    nom: str
    reference: Optional[str]
    date_installation: Optional[datetime]
    statut: Optional[str]
    site_id: Optional[int]

    model_config = {
        "from_attributes": True
    }