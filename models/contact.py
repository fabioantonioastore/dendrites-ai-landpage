from sqlalchemy.orm import mapped_column
from sqlalchemy import String

from models import Base
from utils import uuid4_factory


class Contact(Base):
    __tablename__ = "contacs"

    id = mapped_column(String, primary_key=True, default=uuid4_factory)
    name = mapped_column(String(200))
    email = mapped_column(String(200), unique=True)
    number = mapped_column(String(50), unique=True)
