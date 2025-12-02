from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

config_dict = ConfigDict(str_strip_whitespace=True)

class DanceClass(BaseModel):
    title: str
    instructor: str
    studio: str
    style: str
    date: datetime
    start_time: datetime 
    end_time: datetime 
    difficulty: str
    