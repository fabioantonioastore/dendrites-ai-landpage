from fastapi import FastAPI, Request, Form, status, HTTPException
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi.staticfiles import StaticFiles

import phonenumbers
import re

from crud import ContactCRUD
from models import Contact


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("landpage.html", {"request": request})


@app.post("/")
async def contact_router(
    name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    number: Annotated[str, Form()],
):
    number_obj = phonenumbers.parse(number, "BR")
    if not phonenumbers.is_valid_number(number_obj):
        print("error_phone")
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid phone number"
        )
    pattern = re.compile(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")
    if not re.fullmatch(pattern, email):
        print("error")
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email"
        )
    contact = Contact(
        name=name,
        email=email,
        number=f"+{number_obj.country_code}{number_obj.national_number}",
    )
    try:
        await ContactCRUD.create_contact(contact)
    except Exception as error:
        pass
    finally:
        return status.HTTP_200_OK
