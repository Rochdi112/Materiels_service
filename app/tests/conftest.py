import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.models.materiel_model import User
from app.security import get_current_user


# 🔐 Simuler un utilisateur admin
def override_get_current_user():
    return User(id=1, username="admin", role="admin")  # Simule un user admin

app.dependency_overrides[get_current_user] = override_get_current_user

# 🧪 SQLite in-memory async engine
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(TEST_DATABASE_URL, echo=False)
async_session_test = sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)

# ⚙️ Override get_db
async def override_get_db():
    async with async_session_test() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

# ✅ CORRECT : async fixture compatible avec pytest-asyncio
@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
