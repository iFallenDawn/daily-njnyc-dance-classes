from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from scrapers import ilovedance, modega
from models.models import DanceClass
from data import danceclasses
from datetime import datetime
import asyncio

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get_all_classes(
    title: Annotated[
        str | None,
        Query(
            title="Name of class",
        )                
    ] = None,
    instructor: Annotated[
        str | None,
        Query(
            title="Instructor of class",
        )                
    ] = None,
    studios: Annotated[
        list[str] | None,
        Query(
            title="Name of studio(s)",
            description='Can have multiple: modega, ilovedance, ilovedance manhattan, ilovedance queens, ilovedance new jersey'
        )                
    ] = None,
    style: Annotated[
        str | None,
        Query(
            title="Style of class",
            description='Not implemented yet',
            deprecated=True
        )                
    ] = None,
    date: Annotated[
        datetime | None,
        Query(
            title="Date of class"
        )                
    ] = None,
    start_time: Annotated[
        datetime | None,
        Query(
            title="Start time of class"
        )                
    ] = None,
    end_time: Annotated[
        datetime | None,
        Query(
            title="End time of class"
        )                
    ] = None,
    difficulty: Annotated[
        str | None,
        Query(
            title="Difficulty of class",
            description='Not implemented yet',
            deprecated=True
        )                
    ] = None,
    cancelled: Annotated[
        bool | None,
        Query(
            title="Whether or not class is cancelled"
        )                
    ] = None,
    page: Annotated[
        int,
        Query(
            ge=1,
            title="Page number",
            description="Page number for pagination, starts at 1"
        )
    ] = 1,
    limit: Annotated[
        int,
        Query(
            le=50,
            title="Number of results",
            description="Limit the number of results, max is 50"
        )
    ] = 10
):
    dance_class_data = await danceclasses.get_all_dance_classes(
        title,
        instructor,
        studios,
        style,
        date,
        start_time,
        end_time,
        difficulty,
        cancelled,
        page,
        limit
    )
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