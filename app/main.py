from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.materiels import router as materiels_router
from app.database import init_db


app = FastAPI(
    title="Materiels Service",
    description="Microservice de gestion des matériels pour l’ERP MIF MAROC",
    version="1.0.0",
)


# 🌍 Autoriser le frontend Astro/HTMX en dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔐 à restreindre en prod si besoin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 📦 Routes
app.include_router(materiels_router)


# 🧱 Créer les tables à la première exécution
@app.on_event("startup")
async def on_startup():
    await init_db()
