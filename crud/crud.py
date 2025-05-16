from typing import AsyncIterator, Any

from sqlalchemy.ext.asyncio import AsyncSession

from database import async_session_factory


class CRUD:
    session_factory = async_session_factory

    @classmethod
    async def get_async_session(cls) -> AsyncIterator[AsyncSession]:
        async with async_session_factory() as session:
            yield session
