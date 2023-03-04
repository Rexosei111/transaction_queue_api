from datetime import time
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class ForgotOTP(BaseModel):
    nohp: str


class ResetOTP(BaseModel):
    new_otp: str
    token: str


class NamesCounterCreate(BaseModel):
    nohp: str
    namecounter: str
    address: Optional[str]
    timeclosing: Optional[time]
    location: Optional[str]
    otp: str


class NamesCounterUpdate(BaseModel):
    nohp: Optional[str]
    namecounter: Optional[str]
    address: Optional[str]
    timeclosing: Optional[time]
    location: Optional[str]
    otp: Optional[str]


class NamesCounterRead(BaseModel):
    idcounter: int
    namecounter: str
    nohp: str
    address: Optional[str]
    location: Optional[str]
    timeclosing: Optional[time]

    class Config:
        orm_mode = True


class LoginRead(BaseModel):
    idcounter: int
    namecounter: str
    nohp: str
    address: Optional[str]
    timeclosing: Optional[time]
    access_token: str
    token_type: str


class LoginData(BaseModel):
    nohp: str = Field(description="Unix key")
    otp: str
