from sqlalchemy.ext.asyncio import async_sessionmaker
from database import engine


async_session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
