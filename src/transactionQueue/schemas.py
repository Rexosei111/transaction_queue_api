from datetime import date
from datetime import time
from enum import Enum
from typing import Optional

from namesCounter.schemas import NamesCounterRead
from pydantic import BaseModel
from pydantic import Field


class TransactionQueueRead(BaseModel):
    idqueue: int
    statusclient: str
    statusnumber: Optional[str]
    yournumber: Optional[int]
    idcounter: int
    tnamecounter: NamesCounterRead
    date: date
    timestamp: time

    class Config:
        orm_mode = True


class TransactionQueueUpdate(BaseModel):
    statusnumber: str


class TransactionQueueCreate(BaseModel):
    nohp: str
    statustclient: str
    statusnumber: Optional[str]
    date: Optional[date]
    timestamp: Optional[time]

    class Config:
        orm_mode = True
