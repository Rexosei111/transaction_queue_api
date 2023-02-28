from datetime import date
from datetime import datetime
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
    date: date
    timestamp: datetime
    namecounter: str
    nohp: str
    address: Optional[str]
    location: Optional[str]
    timeclosing: Optional[time]

    class Config:
        orm_mode = True


class TransactionQueueUpdate(BaseModel):
    statusnumber: str


class TransactionQueueCreate(BaseModel):
    idcounter: int
    nohp: str
    statustclient: str
    statusnumber: Optional[str]
    date: Optional[date]
    timestamp: Optional[datetime]

    class Config:
        orm_mode = True
