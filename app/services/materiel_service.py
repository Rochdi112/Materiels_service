from typing import List, Optional
from datetime import datetime
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.materiel_model import Materiel, StatutMateriel
from app.schemas.materiel_schema import (
    MaterielCreate, MaterielUpdate, MaterielStats
)


async def create_materiel(db: AsyncSession, materiel: MaterielCreate) -> Materiel:
    db_materiel = Materiel.model_validate(materiel)
    db.add(db_materiel)
    await db.commit()
    await db.refresh(db_materiel)
    return db_materiel


async def get_all_materiels(
    db: AsyncSession,
    statut: Optional[str] = None,
    site_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[Materiel]:
    query = select(Materiel)
    if statut:
        query = query.where(Materiel.statut == statut)
    if site_id:
        query = query.where(Materiel.site_id == site_id)
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    return result.scalars().all()


async def get_materiel(db: AsyncSession, materiel_id: int) -> Materiel:
    result = await db.execute(select(Materiel).where(Materiel.id == materiel_id))
    materiel = result.scalar_one_or_none()
    if not materiel:
        raise ValueError("Matériel introuvable")
    return materiel


async def update_materiel(
    db: AsyncSession,
    materiel_id: int,
    materiel_update: MaterielUpdate,
    utilisateur: str
) -> Materiel:
    materiel = await get_materiel(db, materiel_id)
    materiel_data = materiel_update.model_dump(exclude_unset=True)

    for key, value in materiel_data.items():
        setattr(materiel, key, value)

    await db.commit()
    await db.refresh(materiel)
    return materiel


async def update_statut(
    db: AsyncSession,
    materiel_id: int,
    statut: StatutMateriel,
    utilisateur: str
) -> Materiel:
    materiel = await get_materiel(db, materiel_id)
    materiel.statut = statut
    await db.commit()
    await db.refresh(materiel)
    return materiel


async def delete_materiel(db: AsyncSession, materiel_id: int):
    materiel = await get_materiel(db, materiel_id)
    await db.delete(materiel)
    await db.commit()


async def search_materiels(db: AsyncSession, query: str) -> List[Materiel]:
    stmt = select(Materiel).where(
        or_(
            Materiel.nom.ilike(f"%{query}%"),
            Materiel.reference.ilike(f"%{query}%")
        )
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_materiels_en_retard(db: AsyncSession) -> List[Materiel]:
    today = datetime.utcnow()
    stmt = select(Materiel).where(
        Materiel.prochaine_maintenance.is_not(None),
        Materiel.prochaine_maintenance < today
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_stats(db: AsyncSession) -> MaterielStats:
    counts = {}
    for statut in StatutMateriel:
        stmt = select(func.count()).where(Materiel.statut == statut)
        result = await db.execute(stmt)
        counts[statut.value] = result.scalar_one()

    total = sum(counts.values())

    return MaterielStats(
        total=total,
        actifs=counts.get("actif", 0),
        en_maintenance=counts.get("en_maintenance", 0),
        hors_service=counts.get("hors_service", 0),
        en_panne=counts.get("en_panne", 0)
    )
    counts = {}
    for statut in StatutMateriel:
        stmt = select(func.count()).where(Materiel.statut == statut)
        result = await db.execute(stmt)
        counts[statut.value] = result.scalar_one()

    return MaterielStats(**counts)
