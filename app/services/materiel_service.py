from sqlmodel import Session, select
from app.models.materiel_model import Materiel
from app.schemas.materiel_schema import MaterielCreate, MaterielRead

async def create_materiel(db: Session, materiel_data: MaterielCreate) -> Materiel:
    materiel = Materiel(**materiel_data.model_dump())
    db.add(materiel)
    db.commit()
    db.refresh(materiel)
    return materiel

async def get_all_materiels(db: Session):
    return db.exec(select(Materiel)).all()

async def update_materiel(db: Session, materiel_id: int, materiel_data) -> Materiel:
    materiel = db.get(Materiel, materiel_id)
    if not materiel:
        raise ValueError("Matériel non trouvé")
    for key, value in materiel_data.model_dump(exclude_unset=True).items():
        setattr(materiel, key, value)

    db.commit()
    db.refresh(materiel)
    return materiel

async def delete_materiel(db: Session, materiel_id: int):
    materiel = db.get(Materiel, materiel_id)
    if not materiel:
        raise ValueError("Matériel non trouvé")
    db.delete(materiel)
    db.commit()