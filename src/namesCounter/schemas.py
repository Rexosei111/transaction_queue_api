from datetime import time
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class NamesCounterCreate(BaseModel):
    nohp: str
    namecounter: str
    address: Optional[str]
    timeclosing: Optional[time]
    otp: str


class NamesCounterUpdate(BaseModel):
    nohp: Optional[str]
    namecounter: Optional[str]
    address: Optional[str]
    timeclosing: Optional[time]
    otp: Optional[str]


class NamesCounterRead(BaseModel):
    idcounter: int
    namecounter: str
    nohp: str
    address: Optional[str]
    timeclosing: Optional[time]

    class Config:
        orm_mode = True


class LoginData(BaseModel):
    nohp: str = Field(description="Unix key")
    otp: str
