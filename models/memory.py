from datetime import datetime

from pydantic import BaseModel


class Memory(BaseModel):
    type: str
    fact: str
    importance: float
    timestamp: datetime