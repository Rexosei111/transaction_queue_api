from typing import List

from database import get_async_session
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from .schemas import LoginData
from .schemas import NamesCounterCreate
from .schemas import NamesCounterRead
from .schemas import NamesCounterUpdate
from .services import add_new_name_counter
from .services import get_list_of_names_counters
from .services import login
from .services import update_names_counter

names_counter_router = APIRouter(prefix="/api/v1/namescounter")


@names_counter_router.get("/", response_model=List[NamesCounterRead])
async def get_names_counters(
    session: Session = Depends(get_async_session),
    limit: int = 10,
    offset: int = 0,
):
    """
    Get the list of namescounters.
    You can paginate the results of this endpoint by setting
    the limit and offset query parameters as needed.

    Maximum of 10 rows are returned by default.
    """
    return await get_list_of_names_counters(session, limit, offset)


@names_counter_router.post("/", response_model=NamesCounterRead)
async def register_name_counter(
    data: NamesCounterCreate, session: Session = Depends(get_async_session)
):
    """
    Register namescounter endpoint
    """
    return await add_new_name_counter(session, data)


@names_counter_router.patch("/{idcounter}", response_model=NamesCounterRead)
async def update_counter(
    *,
    idcounter: int,
    session: Session = Depends(get_async_session),
    update_data: NamesCounterUpdate
):
    """
    Update name counter endpoint"""
    return await update_names_counter(session, idcounter, update_data)


@names_counter_router.post("/login", response_model=NamesCounterRead)
async def login_counter(
    loginData: LoginData, session: Session = Depends(get_async_session)
):
    return await login(session, loginData)
