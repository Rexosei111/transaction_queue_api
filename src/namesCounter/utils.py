import hashlib
import json
import typing
from datetime import datetime
from datetime import timedelta
from typing import Union

from database import get_async_session
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from jose import jwt
from jose import JWTError
from namesCounter.models import TNamesCounter
from settings import get_settings
from sqlalchemy.ext.asyncio import AsyncSession

settings = get_settings()


async def encrypt_otp_with_md5(otp: str):
    return hashlib.md5(otp.encode()).hexdigest()


async def create_access_tokens(
    data: TNamesCounter, expires_delta: Union[timedelta, None] = None
):
    to_encode = {
        "idcounter": data.idcounter,
        "nohp": data.nohp,
        "namecounter": data.namecounter,
    }
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=40)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt_secret, algorithm=settings.algorithm
    )
    return encoded_jwt


class CustomResponse(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        if content is None:
            return b""
        if isinstance(content, bytes):
            return content
        if isinstance(content, dict):
            content = {**content, "codestatus": self.status_code}
            return json.dumps(content).encode(self.charset)
        return content.encode(self.charset)
