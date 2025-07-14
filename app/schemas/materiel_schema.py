from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class StatutMateriel(str, Enum):
    actif = "actif"
    en_maintenance = "en_maintenance"
    hors_service = "hors_service"
    en_panne = "en_panne"


class MaterielBase(BaseModel):
    nom: str = Field(..., min_length=2)
    reference: Optional[str] = Field(default=None, min_length=1)
    date_installation: Optional[datetime] = None
    statut: Optional[StatutMateriel] = StatutMateriel.actif
    site_id: Optional[int] = None
    prochaine_maintenance: Optional[datetime] = None


class MaterielCreate(MaterielBase):
    pass


class MaterielUpdate(BaseModel):
    nom: Optional[str] = None
    reference: Optional[str] = None
    date_installation: Optional[datetime] = None
    statut: Optional[StatutMateriel] = None
    site_id: Optional[int] = None
    prochaine_maintenance: Optional[datetime] = None


class MaterielRead(MaterielBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MaterielStatutUpdate(BaseModel):
    statut: StatutMateriel


class MaterielSearchQuery(BaseModel):
    query: str


class MaterielStats(BaseModel):
    total: int
    actifs: int
    en_maintenance: int
    hors_service: int
    en_panne: int
