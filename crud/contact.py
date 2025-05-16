from typing import AsyncGenerator

from sqlalchemy import select

from crud import CRUD
from models import Contact


class ContactCRUD(CRUD):
    @classmethod
    async def get_all_contacts(cls) -> list[Contact]:
        async with cls.session_factory() as session:
            statement = select(Contact)
            result = await session.execute(statement)
            return result.scalars().all()

    @classmethod
    async def get_all_contacts_gen(cls) -> AsyncGenerator:
        async with cls.session_factory() as session:
            statement = select(Contact)
            result = await session.stream(statement)
            async for contact in result.scalars():
                yield contact

    @classmethod
    async def create_contact(cls, contact: Contact) -> Contact:
        async with cls.session_factory() as session:
            session.add(contact)
            await session.commit()
            return contact

    @classmethod
    async def delete_contact(cls, id: str) -> str:
        async with cls.session_factory() as session:
            try:
                statement = select(Contact).where(Contact.id == id)
                result = await session.execute(statement)
                contact = result.scalars().one()
                await session.delete(contact)
                await session.commit()
                return "deleted"
            except Exception as error:
                await session.rollback()
