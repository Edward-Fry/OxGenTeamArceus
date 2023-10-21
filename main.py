from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import starlette.status as status
import gmaps

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def get_home_page(request: Request):
    return templates.TemplateResponse("home_page.html", {"request": request})

@app.post("/", response_class=RedirectResponse)
def get_home_page(prompt: Annotated[str, Form()]):
    return RedirectResponse(f"/map/{prompt}", status_code=status.HTTP_302_FOUND)

@app.get("/map/{prompt}", response_class=HTMLResponse)
def get_map_page(request: Request, prompt: str):
    locations = gmaps.get_places_images_and_locations_from_text(prompt)
    return templates.TemplateResponse("map_page.html", {"request": request, "prompt": prompt, "locations": locations})

@app.get("/test/{prompt}", response_class=HTMLResponse)
def testtt(request: Request, prompt: str):
    locations = gmaps.get_places_images_and_locations_from_text(prompt)
    return templates.TemplateResponse("test.html", {"request": request, "prompt": prompt, "locations": locations})