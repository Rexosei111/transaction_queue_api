from datetime import date
from datetime import datetime
from datetime import time
from enum import Enum
from typing import Optional

from pydantic import BaseModel
from pydantic import validator


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

    @validator("date")
    def date_must_not_be_in_past(cls, v):
        if v < datetime.date(datetime.now()):
            raise ValueError("Date cannot be in the past")
        return v


class TransactionQueueCreate(BaseModel):
    idcounter: int
    nohpclient: str
    statusclient: str
    statusnumber: Optional[StatusNumberOptions] = StatusNumberOptions.none
    date: Optional[date]
    timestamp: Optional[datetime]

    @validator("timestamp")
    def timestamp_must_not_be_in_past(cls, v):  # type: ignore
        if v < datetime.now():
            raise ValueError("Date cannot be in the past")
        return v

    @validator("date")
    def date_must_not_be_in_past(cls, v):
        if v < datetime.date(datetime.now()):
            raise ValueError("Date cannot be in the past")
        return v

    class Config:
        orm_mode = True
