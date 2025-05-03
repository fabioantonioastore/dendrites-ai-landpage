from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine
from os import getenv


load_dotenv()

engine = create_async_engine(url=getenv("DATABASE_URL"), echo=False)
