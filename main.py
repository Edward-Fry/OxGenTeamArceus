import json
from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import starlette.status as status
import gmaps
import prompt_filtering
import promptToLocation

import uvicorn

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
    MAX_LOCATION_PREDICTIONS = 3
    MAX_PLACES_PER_SEARCH_TEXT = 3

    key_prompt_info = prompt_filtering.extract_key_info_from_prompt(prompt)
    location_predictions = promptToLocation.get_location_predictions(key_prompt_info, MAX_LOCATION_PREDICTIONS)
    locations = []
    print(f"number of location_predictions: {len(location_predictions)}")
    for location_prediction in location_predictions:
        print(f"location_prediction: {location_prediction}")
        locations += gmaps.get_places_images_and_locations_from_text(location_prediction, MAX_PLACES_PER_SEARCH_TEXT)
        print(f"number of locations: {len(locations)} ")
    marker_positions = json.dumps([{"lat": l["lat"], "lng": l["lng"]} for l in locations])
    return templates.TemplateResponse("map_page.html", {"request": request, "prompt": prompt, "locations": locations, "marker_positions": marker_positions})


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)