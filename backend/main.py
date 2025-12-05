from fastapi import FastAPI, Query
from typing import Annotated
from scrapers import ilovedance, modega, bdc
from models.models import DanceClass
import asyncio

app = FastAPI()

@app.get("/")
async def get_all_classes(
    studio: Annotated[
        str | None,
        Query(
            title="Name of studio",
            description='modega, ilovedance, bdc'
        )                
    ] = None
) -> list[DanceClass]:
    if studio:
        studio = studio.lower()
        if studio == 'ilovedance':
            return ilovedance.get_ilovedance_classes()
        elif studio == 'modega':
            return modega.get_modega_classes()
        elif studio == 'bdc':
            return bdc.get_bdc_classes()
        else: 
            return []
    else:
        loop = asyncio.get_event_loop()
        ilovedance_task = loop.run_in_executor(None, ilovedance.get_ilovedance_classes)
        modega_task = loop.run_in_executor(None, modega.get_modega_classes)
        bdc_task = loop.run_in_executor(None, bdc.get_bdc_classes)
        
        ilovedance_results, modega_results, bdc_results = await asyncio.gather(
            ilovedance_task,
            modega_task,
            bdc_task
        )
        dance_class_data = []
        dance_class_data.extend(ilovedance_results)
        dance_class_data.extend(modega_results)
        dance_class_data.extend(bdc_results)
        return dance_class_data
