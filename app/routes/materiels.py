from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_db
from app.models.materiel_model import Materiel, MaterielUpdate
from app.schemas.materiel_schema import MaterielCreate
from app.services.materiel_service import (
    create_materiel, get_all_materiels,
    update_materiel, delete_materiel
)

router = APIRouter(prefix="/materiels", tags=["Materiels"])

@router.post("/", response_model=Materiel)
async def create(materiel: MaterielCreate, db: Session = Depends(get_db)):
    return await create_materiel(db, materiel)

@router.get("/", response_model=list[Materiel])
async def read_all(db: Session = Depends(get_db)):
    return await get_all_materiels(db)

@router.put("/{materiel_id}", response_model=Materiel)
async def update(materiel_id: int, materiel: MaterielUpdate, db: Session = Depends(get_db)):
    try:
        return await update_materiel(db, materiel_id, materiel)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{materiel_id}")
async def delete(materiel_id: int, db: Session = Depends(get_db)):
    try:
        await delete_materiel(db, materiel_id)
        return {"message": "Matériel supprimé avec succès"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
