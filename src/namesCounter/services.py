from typing import List

from fastapi import HTTPException
from fastapi import status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import TNamesCounter
from .schemas import LoginData
from .schemas import NamesCounterCreate
from .schemas import NamesCounterUpdate
from .utils import create_access_tokens
from .utils import encrypt_otp_with_md5


async def add_new_name_counter(
    session: AsyncSession, data: NamesCounterCreate
) -> TNamesCounter:
    data_dict = data.dict()
    otp = await encrypt_otp_with_md5(data_dict.pop("otp"))
    new_name_counter = TNamesCounter(**data_dict, otp=otp)
    try:
        session.add(new_name_counter)
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            detail="tnamecounter already exist",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    await session.refresh(new_name_counter)
    return new_name_counter


async def get_names_counter_by_id(
    session: AsyncSession, idcounter: int
) -> TNamesCounter:
    statement = select(TNamesCounter).where(TNamesCounter.idcounter == idcounter)
    try:
        names_counter = await session.scalar(statement)
        if names_counter is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"namecounter with idcounter {idcounter} does not exist",
            )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve data at this time",
        )

    return names_counter


async def get_names_counter_by_nohp(session: AsyncSession, nohp: str) -> TNamesCounter:
    statement = select(TNamesCounter).where(TNamesCounter.nohp == nohp)
    try:
        names_counter = await session.scalar(statement)
        if names_counter is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"namecounter with nohp {nohp} does not exist",
            )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve data at this time",
        )

    return names_counter


async def get_list_of_names_counters(
    session: AsyncSession, limit: int, offset: int, namecounter: str, address: str
) -> List[TNamesCounter]:
    statement = (
        select(TNamesCounter)
        .filter(
            TNamesCounter.namecounter.like(f"%{namecounter}%"),
            TNamesCounter.address.like(f"%{address}%"),
        )
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
    session: AsyncSession,
    nohp: str,
    data: NamesCounterUpdate,
) -> TNamesCounter:
    names_counter = await get_names_counter_by_nohp(session, nohp)
    for key, value in data.dict(exclude_unset=True).items():
        if key == "otp":
            value = await encrypt_otp_with_md5(value)
        setattr(names_counter, key, value)

    try:
        await session.commit()
    except SQLAlchemyError:
        raise HTTPException(
            detail="Unable to retrieve data at this time",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    await session.refresh(names_counter)
    return names_counter


async def login(session: AsyncSession, loginData: LoginData):
    statement = select(TNamesCounter).where(TNamesCounter.nohp == loginData.nohp)
    try:
        names_counter = await session.scalar(statement)
        if names_counter is None:
            raise HTTPException(
                detail="namecounter does not exist",
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    except SQLAlchemyError:
        raise HTTPException(
            detail="Unable to retrieve data at this time",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    if names_counter.otp != await encrypt_otp_with_md5(loginData.otp):
        raise HTTPException(
            detail="Invalid OTP",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    access_token = await create_access_tokens(names_counter)
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        **names_counter.__dict__,
    }
