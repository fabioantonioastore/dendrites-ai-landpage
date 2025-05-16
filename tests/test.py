from crud import ContactCRUD
from asyncio import run

async def main():
    contacts = await ContactCRUD.get_all_contacts()
    for contact in contacts:
        print(contact.name, contact.email, contact.number, contact.id)
        await ContactCRUD.delete_contact(contact.id)

run(main())