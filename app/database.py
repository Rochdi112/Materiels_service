from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession  # ✅
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# 🛠️ URL de connexion SQLite asynchrone
DATABASE_URL = "sqlite+aiosqlite:///./materiels.db"

# 🚀 Moteur asynchrone
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

# 🧵 Fabrique de sessions
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# 🧱 Création des tables (exécuté manuellement ou via startup event)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


# ✅ Ajoute ceci pour éviter l’erreur ImportError
def get_db():
    return async_session
