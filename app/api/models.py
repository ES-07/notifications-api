import datetime
from pydantic import BaseModel
from typing import Union

class Intrusion(BaseModel):
    timestamp: datetime.datetime
    camera_id: int
    frame_id: int
    email: Union[str, None] = None
