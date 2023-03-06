from datetime import date
from datetime import datetime
from datetime import time
from enum import Enum
from typing import Optional

from namesCounter.schemas import NamesCounterRead
from pydantic import BaseModel
from pydantic import Field


class StatusClientOptions(str, Enum):
    emum = "emum"
    bpjs = "bpjs"
    asuransi = "asuransi"


class StatusNumberOptions(str, Enum):
    none = "none"
    cancel = "cancel"
    skip = "skip"
    void = "void"
    hold = "hold"
    closing = "closing"


class TransactionQueueRead(BaseModel):
    idqueue: int
    statusclient: str
    statusnumber: Optional[str]
    yournumber: Optional[int]
    idcounter: int
    date: date
    timestamp: datetime
    namecounter: str
    nohpclient: str
    address: Optional[str]
    location: Optional[str]
    timeclosing: Optional[time]
    posnumber: int
    endnumber: int

    class Config:
        orm_mode = True


class TransactionQueueUpdate(BaseModel):
    idcounter: int
    nohpclient: str
    statusnumber: StatusNumberOptions
    date: Optional[date]
    statusclient: str


class TransactionQueueCreate(BaseModel):
    idcounter: int
    nohpclient: str
    statusclient: str
    statusnumber: Optional[StatusNumberOptions] = StatusNumberOptions.none
    date: Optional[date]
    timestamp: Optional[datetime]

    class Config:
        orm_mode = True
