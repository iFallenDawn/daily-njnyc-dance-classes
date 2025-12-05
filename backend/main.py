from fastapi import FastAPI, Query
from typing import Annotated
from scrapers import ilovedance, modega
from models.models import DanceClass
from data import danceclasses
import asyncio

app = FastAPI()

@app.get("/")
async def get_all_classes(
    studio: Annotated[
        str | None,
        Query(
            title="Name of studio",
            description='modega, ilovedance, ilovedance manhattan, ilovedance queens, ilovedance new jersey'
        )                
    ] = None
):
    if studio:
        return await danceclasses.get_dance_classes_by_studio(studio)
    dance_class_data = await danceclasses.get_all_dance_classes()
    return dance_class_data

@app.get('/scrape')
async def scrape_all_classes() -> list[DanceClass]:
    loop = asyncio.get_event_loop()
    ilovedance_task = loop.run_in_executor(None, ilovedance.get_ilovedance_classes)
    modega_task = loop.run_in_executor(None, modega.get_modega_classes)
    
    ilovedance_results, modega_results = await asyncio.gather(
        ilovedance_task,
        modega_task
    )
    dance_class_data = []
    dance_class_data.extend(ilovedance_results)
    dance_class_data.extend(modega_results)
    await danceclasses.delete_all_dance_classes()
    return await danceclasses.create_dance_classes(dance_class_data)