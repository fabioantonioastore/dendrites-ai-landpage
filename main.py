from fastapi import FastAPI, HTTPException, status
from email_validator import validate_email

from crud import EmailCRUD
from models import Email


app = FastAPI()


@app.get("/")
async def root():
    pass


@app.get("/emails")
async def get_all_emails_router():
    return await EmailCRUD.get_all_emails()


@app.post("/{email}")
async def create_email_router(email: str):
    if not validate_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email"
        )
    email_model = Email()
    email_model.email = email
    return await EmailCRUD.create_email(email_model)
