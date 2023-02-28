from datetime import date
from typing import List

from fastapi import HTTPException
from fastapi import status
from namesCounter.services import get_names_counter_by_nohp
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import TransactionQueue
from .schemas import TransactionQueueCreate
from .schemas import TransactionQueueUpdate


async def get_queues(session: AsyncSession, data: TransactionQueueCreate):
    statement = (
        select(TransactionQueue)
        .where(
            TransactionQueue.idcounter == data.idcounter,
            TransactionQueue.date == data.date,
            TransactionQueue.statusclient == data.statustclient,
            TransactionQueue.statusnumber == data.statusnumber,
        )
        .options(selectinload(TransactionQueue.tnamecounter))
    )
    try:
        queues = await session.execute(statement)
        queues = queues.scalars().all()
    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to retrieve data at this time",
        )
    return queues


async def get_queues_by_query_params(
    session: AsyncSession,
    # idcounter: int,
    nohp,
    date: date,
    statusclient: str,
    statusnumber: str,
):
    name_counter = await get_names_counter_by_nohp(session=session, nohp=nohp)
    idcounter = name_counter.idcounter
    statement = (
        select(TransactionQueue)
        .where(
            TransactionQueue.idcounter == idcounter,
            TransactionQueue.date == date,
            TransactionQueue.statusclient == statusclient,
            TransactionQueue.statusnumber == statusnumber,
        )
        .options(selectinload(TransactionQueue.tnamecounter))
    )
    try:
        queues = await session.execute(statement)
        queues = queues.scalars().all()
    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to retrieve data at this time",
        )
    return queues


async def get_queues_by_nohp_and_date(
    session: AsyncSession,
    # idcounter: int,
    nohp,
    date: date,
):
    name_counter = await get_names_counter_by_nohp(session=session, nohp=nohp)
    idcounter = name_counter.idcounter
    statement = (
        select(TransactionQueue)
        .where(TransactionQueue.idcounter == idcounter, TransactionQueue.date == date)
        .options(selectinload(TransactionQueue.tnamecounter))
    )
    try:
        queue = await session.scalar(statement)
    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to retrieve data at this time",
        )
    return queue


async def get_queues_by_date(
    session: AsyncSession,
    date: date,
):
    statement = (
        select(TransactionQueue)
        .where(TransactionQueue.date == date)
        .options(selectinload(TransactionQueue.tnamecounter))
    )
    try:
        queues = await session.execute(statement)
        queues = queues.all()
    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to retrieve data at this time",
        )
    return queues


async def get_queue_by_id(session: AsyncSession, idqueue: int):
    statement = (
        select(TransactionQueue)
        .where(TransactionQueue.idqueue == idqueue)
        .options(selectinload(TransactionQueue.tnamecounter))
    )
    try:
        queue = await session.scalar(statement)
        if queue is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to retrieve data at this time",
        )
    return queue


async def create_queue(session: AsyncSession, data: TransactionQueueCreate):
    current_name_counter = await get_names_counter_by_nohp(
        session=session, nohp=data.nohp
    )
    existing_queue = await get_queues_by_nohp_and_date(
        session, current_name_counter.nohp, date=data.date
    )
    if existing_queue is not None:
        return existing_queue
    queues = await get_queues_by_date(session, data.date)
    queue = TransactionQueue(
        idcounter=current_name_counter.idcounter,
        tnamecounter=current_name_counter,
        statusclient=data.statustclient,
        statusnumber=data.statusnumber,
        yournumber=len(queues) + 1,
        timestamp=data.timestamp,
        date=data.date,
    )
    try:
        session.add(queue)
        await session.commit()
        await session.refresh(queue)
    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to retrieve data at this time",
        )
    queue = await get_queue_by_id(session, queue.idqueue)
    return queue


async def update_queue(
    session: AsyncSession,
    idqueue: int,
    data: TransactionQueueUpdate,
    current_name_counter,
):
    queue = await get_queue_by_id(session, idqueue)
    if queue.idcounter != current_name_counter.idcounter:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are unauthorized to perform this operaiton",
        )
    queue.statusnumber = data.statusnumber
    try:
        session.add(queue)
        await session.commit()
        await session.refresh(queue)
    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to retrieve data at this time",
        )
    return queue
