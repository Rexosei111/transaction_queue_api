from datetime import date
from typing import List
from typing import Optional

from database import get_async_session
from fastapi import APIRouter
from fastapi import Depends
from namesCounter.router import get_current_name_counter
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import TransactionQueueCreate
from .schemas import TransactionQueueRead
from .schemas import TransactionQueueUpdate
from .services import create_queue
from .services import get_queues_by_query_params
from .services import update_queue

transaction_queue_router = APIRouter(prefix="/api/v1/queues")


@transaction_queue_router.post("/", response_model=TransactionQueueRead)
async def add_queue(
    data: TransactionQueueCreate,
    session: AsyncSession = Depends(get_async_session),
    current_name_counter=Depends(get_current_name_counter),
):
    return await create_queue(session, data, current_name_counter)


# @transaction_queue_router.post("/queue", response_model=List[TransactionQueueRead])
# async def get_queues_obj(
#     *, session: AsyncSession = Depends(get_async_session), data: TransactionQueueCreate
# ):
#     return await get_queues(session, data)


@transaction_queue_router.patch("/{idqueue}", response_model=TransactionQueueRead)
async def edit_queue(
    *,
    idqueue: int,
    session: AsyncSession = Depends(get_async_session),
    data: TransactionQueueUpdate,
    current_name_counter=Depends(get_current_name_counter)
):
    return await update_queue(session, idqueue, data, current_name_counter)


@transaction_queue_router.get("/", response_model=List[TransactionQueueRead])
async def get_list_of_queues(
    *,
    session: AsyncSession = Depends(get_async_session),
    nohp: Optional[str] = None,
    idcounter: int,
    date: date,
    statusclient: str,
    statusnumber: str,
    current_name_counter=Depends(get_current_name_counter)
):
    return await get_queues_by_query_params(
        session, nohp, idcounter, date, statusclient, statusnumber
    )
