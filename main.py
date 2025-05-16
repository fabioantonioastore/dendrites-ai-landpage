from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi.staticfiles import StaticFiles


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
        number: Annotated[str, Form()]
):
    print(name)
    print(email)
    print(number)