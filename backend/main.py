from fastapi import FastAPI
from scrapers import ilovedance
from models.models import DanceClass

app = FastAPI()

@app.get("/")
def get_all_classes() -> list[DanceClass]:
    return ilovedance.get_ilovedance_classes()