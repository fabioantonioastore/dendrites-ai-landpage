from typing import Iterable, AsyncIterator

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi import HTTPException

from crud import CRUD
from models import Email


class EmailCRUD(CRUD):
    @classmethod
    async def get_all_emails(cls) -> list[Email]:
        async with cls.session_factory() as session:
            statement = select(Email)
            result = await session.execute(statement)
            return result.scalars().all()

    @classmethod
    async def async_get_all_emails(cls) -> AsyncIterator[Email]:
        async with cls.session_factory() as session:
            statement = select(Email)
            result = await session.execute(statement)
            for email in result.scalars():
                yield email

    @classmethod
    async def get_email_by_str(cls, email: str) -> Email | None:
        async with cls.session_factory() as session:
            try:
                statement = select(Email).where(Email.email == email)
                result = await session.execute(statement)
                return result.scalars().one()
            except NoResultFound:
                return None

    @classmethod
    async def get_emails_by_str(cls, emails: Iterable[str]) -> list[Email]:
        async with cls.session_factory() as session:
            try:
                statement = select(Email).where(Email.email in emails)
                result = await session.execute(statement)
                return result.scalars().all()
            except HTTPException as error:
                raise error

    @classmethod
    async def create_email(cls, email: Email) -> Email | None:
        async with cls.session_factory() as session:
            try:
                session.add(email)
                await session.commit()
                return email
            except IntegrityError as error:
                await session.rollback()
                return None

    @classmethod
    async def create_emails(cls, emails: Iterable[Email]) -> Iterable[Email]:
        async with cls.session_factory() as session:
            try:
                for email in emails:
                    session.add(email)
                await session.commit()
                return emails
            except HTTPException as error:
                await session.rollback()
                raise error

    @classmethod
    async def delete_email(cls, email: Email) -> str:
        async with cls.session_factory() as session:
            try:
                await session.delete(email)
                await session.commit()
                return "deleted"
            except HTTPException as error:
                await session.rollback()
                raise error

    @classmethod
    async def delete_email_by_str(cls, email: str) -> str:
        async with cls.session_factory() as session:
            try:
                statement = select(Email).where(Email.email == email)
                result = await session.execute(statement)
                email = result.scalars().one()
                await session.delete(email)
                return "deleted"
            except HTTPException as error:
                await session.rollback()
                raise error

    @classmethod
    async def delete_emails(cls, emails: Iterable[Email]) -> str:
        async with cls.session_factory() as session:
            try:
                for email in emails:
                    await session.delete(email)
                await session.commit()
                return "deleted"
            except HTTPException as error:
                await session.rollback()
                raise error

    @classmethod
    async def delete_emails_by_str(cls, emails: Iterable[str]) -> str:
        async with cls.session_factory() as session:
            try:
                statement = select(Email).where(Email.email in emails)
                result = await session.execute(statement)
                async for email in result.scalars():
                    await session.delete(email)
                await session.commit()
                return "deleted"
            except HTTPException as error:
                await session.rollback()
                raise error

    @classmethod
    async def delete_all(cls) -> str:
        async with cls.session_factory() as session:
            try:
                statement = select(Email)
                result = await session.stream(statement)
                async for email in result.scalars():
                    await session.delete(email)
                await session.commit()
                return "deleted"
            except Exception as error:
                raise error