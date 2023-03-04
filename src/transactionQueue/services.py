from datetime import date
from typing import List

from fastapi import HTTPException
from fastapi import status
from namesCounter.services import get_names_counter_by_id
from namesCounter.services import get_names_counter_by_nohp
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import TransactionQueue
from .schemas import StatusNumberOptions
from .schemas import TransactionQueueCreate
from .schemas import TransactionQueueUpdate
from sqlalchemy.sql.expression import or_

async def get_queues_by_query_params(
    session: AsyncSession,
    idcounter: int,
    date: date,
    statusclient: str,
    statusnumber: str,
):
    statement = (
        select(TransactionQueue)
        .where(
            TransactionQueue.idcounter == idcounter,
            TransactionQueue.date == date,
            TransactionQueue.statusclient.like(f"%{statusclient}%"),
            TransactionQueue.statusnumber.like(f"%{statusnumber}%")
        )
        .options(selectinload(TransactionQueue.tnamecounter))
    )
    try:
        queues = await session.execute(statement)
        queues = queues.scalars().all()
        #if not queues:
         #   raise HTTPException(
          #      status_code=status.HTTP_404_NOT_FOUND,
           #     detail="Queue with these details does not exist",
#            )
    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="unable to retrieve data at this time",
        )
    return queues


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


async def get_queues_count_by_date(
    session: AsyncSession,
    date: date,
):
    statement = select(TransactionQueue).where(TransactionQueue.date == date)
    try:
        queues = await session.execute(statement)
        queues = len(queues.all())
    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to retrieve data at this time",
        )
    return queues


async def get_queues_by_statusnumber(session: AsyncSession, date: date):
    statement = select(TransactionQueue).filter(or_(
        TransactionQueue.statusnumber == "hold", TransactionQueue.statusnumber == "closing"),
        TransactionQueue.date == date,
    )
    try:
        queues = await session.execute(statement)
        queues_count = len(queues.all())
        print(queues_count)
    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to retrieve data at this time",
        )
    return queues_count


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
    statement = (
        select(TransactionQueue)
        .where(
            TransactionQueue.idcounter == data.idcounter,
            TransactionQueue.nohpclient == data.nohpclient,
            TransactionQueue.date == data.date,
        )
        .options(selectinload(TransactionQueue.tnamecounter))
    )
    try:
        existing_queue = await session.execute(statement)
        existing_queue = existing_queue.scalar_one_or_none()
    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve data at this time",
        )

    if existing_queue:
        return existing_queue
    queues = await get_queues_by_date(session, data.date)
    current_name_counter = await get_names_counter_by_id(
        session=session, idcounter=data.idcounter
    )
    queue = TransactionQueue(
        idcounter=current_name_counter.idcounter,
        tnamecounter=current_name_counter,
        statusclient=data.statusclient,
        statusnumber=data.statusnumber,
        nohpclient=data.nohpclient,
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
    session: AsyncSession, data: TransactionQueueUpdate, current_name_counter
):
    statement = (
        select(TransactionQueue)
        .where(
            TransactionQueue.idcounter == data.idcounter,
            TransactionQueue.nohpclient == data.nohpclient,
            TransactionQueue.date == data.date,
        )
        .options(selectinload(TransactionQueue.tnamecounter))
    )
    try:
        existing_queue = await session.execute(statement)
        existing_queue = existing_queue.scalar_one_or_none()
    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to retrieve data at this time",
        )

    if not existing_queue:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"Queue with these details does not exist"
        )

    if existing_queue.idcounter != current_name_counter.idcounter:
        raise HTTPException(403, detail="You are unathorised to edit this queue")
    existing_queue.statusnumber = data.statusnumber
    try:
        session.add(existing_queue)
        await session.commit()
        await session.refresh(existing_queue)
    except SQLAlchemyError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"unable to retrieve data at this time",
        )
    return existing_queue
