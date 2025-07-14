from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


class StatutMateriel(str, Enum):
    actif = "actif"
    en_maintenance = "en_maintenance"
    hors_service = "hors_service"
    en_panne = "en_panne"

class User(SQLModel):
    id: int
    username: str
    role: str
    
class MaterielBase(SQLModel):
    nom: str = Field(index=True)
    reference: Optional[str] = Field(default=None, index=True)
    date_installation: Optional[datetime] = None
    statut: StatutMateriel = Field(default=StatutMateriel.actif)
    site_id: Optional[int] = Field(default=None, index=True)
    prochaine_maintenance: Optional[datetime] = None


class Materiel(MaterielBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    __tablename__ = "materiels"


class MaterielLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    materiel_id: int = Field(foreign_key="materiels.id")
    champ_modifie: str
    ancienne_valeur: Optional[str] = None
    nouvelle_valeur: Optional[str] = None
    date_modification: datetime = Field(default_factory=datetime.utcnow)
    utilisateur: Optional[str] = None
