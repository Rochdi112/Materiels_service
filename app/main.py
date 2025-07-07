from fastapi import FastAPI
from app.routes.materiels import router as materiels_router

app = FastAPI(title="Materiels Service")
app.include_router(materiels_router)