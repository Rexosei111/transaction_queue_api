import json
import typing
from typing import List

from database import get_async_session
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException
from fastapi import status
from jose import jwt
from jose import JWTError
from settings import get_settings
from sqlalchemy.ext.asyncio import AsyncSession

from .exceptions import StatusModel400
from .exceptions import StatusModel401
from .exceptions import StatusModel404
from .schemas import LoginData
from .schemas import LoginRead
from .schemas import NamesCounterCreate
from .schemas import NamesCounterRead
from .schemas import NamesCounterUpdate
from .services import add_new_name_counter
from .services import get_list_of_names_counters
from .services import get_names_counter_by_id
from .services import login
from .services import update_names_counter
from .utils import CustomResponse


settings = get_settings()


async def get_current_name_counter(
    authorization: str = Header(), session: AsyncSession = Depends(get_async_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    authorization = authorization.split(" ")[-1]
    try:
        payload = jwt.decode(
            authorization, settings.jwt_secret, algorithms=[settings.algorithm]
        )
        idcounter: str = payload.get("idcounter")
        if idcounter is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    name_counter = await get_names_counter_by_id(session, idcounter)
    return name_counter


names_counter_router = APIRouter(
    prefix="/api/v1/namescounter",
    responses={
        400: {"model": StatusModel400},
        401: {"model": StatusModel401},
        404: {"model": StatusModel404},
    },
)


@names_counter_router.get("/", response_model=List[NamesCounterRead])
async def get_names_counters(
    *,
    session: AsyncSession = Depends(get_async_session),
    limit: int = 10,
    offset: int = 0,
    namecounter: str = "",
    address: str = "",
):
    """
    Get the list of namescounters.
    You can paginate the results of this endpoint by setting
    the limit and offset query parameters as needed.

    Maximum of 10 rows are returned by default.
    """
    return await get_list_of_names_counters(
        session, limit, offset, namecounter=namecounter, address=address
    )


@names_counter_router.post(
    "/",
    response_model=NamesCounterRead,
    status_code=status.HTTP_200_OK,
    response_class=CustomResponse,
)
async def register_name_counter(
    data: NamesCounterCreate, session: AsyncSession = Depends(get_async_session)
):
    """
    Register namescounter endpoint
    """
    return await add_new_name_counter(session, data)


@names_counter_router.put(
    "/{nohp}", response_model=NamesCounterRead, response_class=CustomResponse
)
async def update_counter(
    *,
    nohp: str,
    session: AsyncSession = Depends(get_async_session),
    update_data: NamesCounterUpdate,
):
    """
    Update name counter endpoint"""
    return await update_names_counter(session, nohp, update_data)


@names_counter_router.post(
    "/login", response_model=LoginRead, response_class=CustomResponse
)
async def login_counter(
    loginData: LoginData, session: AsyncSession = Depends(get_async_session)
):
    return await login(session, loginData)
