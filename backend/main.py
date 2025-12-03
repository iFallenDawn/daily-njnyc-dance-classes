from fastapi import FastAPI, Query
from typing import Annotated
from scrapers import ilovedance, modega
from models.models import DanceClass
import asyncio

app = FastAPI()

@app.get("/")
async def get_all_classes(
    studio: Annotated[
        str | None,
        Query(
            title="Name of studio",
            description='modega, ilovedance'
        )                
    ] = None
) -> list[DanceClass]:
    if studio:
        studio = studio.lower()
        if studio == 'ilovedance':
            return ilovedance.get_ilovedance_classes()
        elif studio == 'modega':
            return modega.get_modega_classes()
        else: 
            return []
    else:
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
        return dance_class_data
