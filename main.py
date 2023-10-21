from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def get_home_page(request: Request):
    return templates.TemplateResponse("home_page.html", {"request": request})

@app.get("/map", response_class=HTMLResponse)
def get_map_page(request: Request):
    return templates.TemplateResponse("map_page.html", {"request": request})
