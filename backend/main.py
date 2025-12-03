from fastapi import FastAPI
from scrapers import ilovedance, modega
from models.models import DanceClass

app = FastAPI()

@app.get("/")
def get_all_classes() -> list[DanceClass]:
    dance_class_data = []
    dance_class_data.extend(ilovedance.get_ilovedance_classes())
    dance_class_data.extend(modega.get_modega_classes())
    return dance_class_data


@app.get("/ilovedance")
def get_ilovedance_classes() -> list[DanceClass]:
    return ilovedance.get_ilovedance_classes()

@app.get("/modega")
def get_modega_classes() -> list[DanceClass]:
    return modega.get_modega_classes()
