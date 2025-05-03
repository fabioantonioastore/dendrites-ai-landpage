from models import Base
from sqlalchemy import String
from sqlalchemy.orm import mapped_column


class Email(Base):
    __tablename__ = "emails"

    email = mapped_column(String, unique=True)
