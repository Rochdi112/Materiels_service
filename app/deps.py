from typing import AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession  # ✅
from app.database import async_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
        await session.commit()
#         await session.refresh(materiel)