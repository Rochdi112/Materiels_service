from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class MaterielBase(SQLModel):
    nom: str
    reference: Optional[str] = None
    date_installation: Optional[datetime] = None
    statut: Optional[str] = "actif"
    site_id: Optional[int] = None

class Materiel(MaterielBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class MaterielRead(MaterielBase):
    id: int

class MaterielUpdate(SQLModel):
    nom: Optional[str] = None
    reference: Optional[str] = None
    date_installation: Optional[datetime] = None
    statut: Optional[str] = None
    site_id: Optional[int] = None