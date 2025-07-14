from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database import get_db
from app.security import admin_required, get_current_user
from app.services import materiel_service
from app.schemas.materiel_schema import (
    MaterielCreate, MaterielRead, MaterielUpdate,
    MaterielStatutUpdate, MaterielStats
)
from app.models.materiel_model import StatutMateriel
from app.models.user_model import User  # si pas déjà importé

router = APIRouter(
    prefix="/materiels",
    tags=["Materiels"]
)

@router.post("/", response_model=MaterielRead, status_code=201)
async def create_materiel(
    materiel: MaterielCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(admin_required),
):
    return await materiel_service.create_materiel(db, materiel)

@router.get("/", response_model=list[MaterielRead])
async def get_all_materiels(
    statut: Optional[StatutMateriel] = Query(None),
    site_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await materiel_service.get_all_materiels(
        db, statut=statut, site_id=site_id, skip=skip, limit=limit
    )

@router.get("/search/", response_model=list[MaterielRead])
async def search(
    query: str = Query(..., min_length=2),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await materiel_service.search_materiels(db, query)

@router.get("/en-retard/", response_model=list[MaterielRead])
async def get_materiels_en_retard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await materiel_service.get_materiels_en_retard(db)

@router.get("/stats", response_model=MaterielStats)
async def get_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await materiel_service.get_stats(db)

@router.get("/{materiel_id}", response_model=MaterielRead)
async def get_one_materiel(
    materiel_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return await materiel_service.get_materiel(db, materiel_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{materiel_id}", response_model=MaterielRead)
async def update_materiel(
    materiel_id: int,
    materiel: MaterielUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(admin_required),
):
    try:
        return await materiel_service.update_materiel(
            db, materiel_id, materiel, utilisateur=current_user.role
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.patch("/{materiel_id}/statut", response_model=MaterielRead)
async def patch_statut(
    materiel_id: int,
    payload: MaterielStatutUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(admin_required),
):
    try:
        return await materiel_service.update_statut(
            db, materiel_id, payload.statut, utilisateur=current_user.role
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{materiel_id}", status_code=200)
async def delete_materiel(
    materiel_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(admin_required),
):
    try:
        await materiel_service.delete_materiel(db, materiel_id)
        return {"message": "Matériel supprimé avec succès"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
