from typing import List

from fastapi import HTTPException
from fastapi import status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .models import TNamesCounter
from .schemas import LoginData
from .schemas import NamesCounterCreate
from .schemas import NamesCounterUpdate
from .utils import encrypt_otp_with_md5


async def add_new_name_counter(
    session: Session, data: NamesCounterCreate
) -> TNamesCounter:
    data_dict = data.dict()
    otp = await encrypt_otp_with_md5(data_dict.pop("otp"))
    new_name_counter = TNamesCounter(**data_dict, otp=otp)
    session.add(new_name_counter)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"tnamecounter with nohp value {new_name_counter.nohp} already exist",
        )
    await session.refresh(new_name_counter)
    return new_name_counter


async def get_names_counter_by_id(session: Session, idcounter: int) -> TNamesCounter:
    statement = select(TNamesCounter).where(TNamesCounter.idcounter == idcounter)
    try:
        names_counter = await session.scalar(statement)
        if names_counter is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"namecounter with idcounter {idcounter} not found",
            )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve data at this time",
        )

    return names_counter


async def get_list_of_names_counters(
    session: Session, limit: int, offset: int
) -> List[TNamesCounter]:
    statement = (
        select(TNamesCounter)
        .limit(limit)
        .offset(offset)
        .order_by(TNamesCounter.namecounter)
    )
    try:
        name_counters = await session.execute(statement)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve data at this time",
        )
    return name_counters.scalars().all()


async def update_names_counter(
    session: Session, idcounter: int, data: NamesCounterUpdate
) -> TNamesCounter:
    names_counter = await get_names_counter_by_id(session, idcounter)
    for key, value in data.dict(exclude_unset=True).items():
        if key == "otp":
            value = await encrypt_otp_with_md5(value)
        setattr(names_counter, key, value)

    try:
        await session.commit()
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve data at this time",
        )
    await session.refresh(names_counter)
    return names_counter


async def login(session: Session, loginData: LoginData):
    statement = select(TNamesCounter).where(
        TNamesCounter.nohp == loginData.nohp,
        TNamesCounter.otp == await encrypt_otp_with_md5(loginData.otp),
    )
    try:
        names_counter = await session.scalar(statement)
        if names_counter is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="namecounter not found"
            )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve data at this time",
        )
    return names_counter
