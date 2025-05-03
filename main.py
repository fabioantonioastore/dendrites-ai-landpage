from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from email_validator import validate_email, EmailNotValidError
from validators import email as validator_email
from validators import ValidationError

from crud import EmailCRUD
from models import Email


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("coming_soon.html", {"request": request})


@app.get("/emails")
async def get_all_emails_router():
    return await EmailCRUD.get_all_emails()


@app.post("/")
async def create_email_router(request: Request, email: str = Form(...)):
    if validator_email(email):
        email_model = Email()
        email_model.email = email
        await EmailCRUD.create_email(email_model)
        return templates.TemplateResponse("thanks.html", {"request": request, "email": email})
    else:
        return templates.TemplateResponse("invalid.html", {"request": request, "email": email})
