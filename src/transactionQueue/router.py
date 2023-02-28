from datetime import date
from typing import Dict
from typing import List

from database import get_async_session
from fastapi import APIRouter
from fastapi import Depends
from namesCounter.models import TNamesCounter
from namesCounter.router import get_current_name_counter
from namesCounter.utils import CustomResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .models import TransactionQueue
from .schemas import TransactionQueueCreate
from .schemas import TransactionQueueRead
from .schemas import TransactionQueueUpdate
from .services import create_queue
from .services import get_queues_by_query_params
from .services import update_queue

transaction_queue_router = APIRouter(prefix="/api/v1/queues")


def transform_queue_data(queue: TransactionQueue):
    queue_dict = queue.__dict__
    tnamecounter: TNamesCounter = queue_dict.pop("tnamecounter")
    tnamecounter: Dict[str, any] = tnamecounter.__dict__
    print(tnamecounter)
    queue_dict = {**queue_dict, **tnamecounter}
    return queue_dict


@transaction_queue_router.post(
    "/",
    response_model=TransactionQueueRead,
    response_class=CustomResponse,
    status_code=201,
)
async def add_queue(
    data: TransactionQueueCreate,
    session: AsyncSession = Depends(get_async_session),
):
    queue = await create_queue(session, data)
    queue_dict = transform_queue_data(queue)
    return queue_dict


# @transaction_queue_router.post("/queue", response_model=List[TransactionQueueRead])
# async def get_queues_obj(
#     *, session: AsyncSession = Depends(get_async_session), data: TransactionQueueCreate
# ):
#     return await get_queues(session, data)


@transaction_queue_router.put(
    "/{idqueue}", response_model=TransactionQueueRead, response_class=CustomResponse
)
async def edit_queue(
    *,
    idqueue: int,
    session: AsyncSession = Depends(get_async_session),
    data: TransactionQueueUpdate,
    current_name_counter=Depends(get_current_name_counter),
):
    queue = await update_queue(session, idqueue, data, current_name_counter)
    queue_dict = transform_queue_data(queue)
    return queue_dict


@transaction_queue_router.get("/", response_model=List[TransactionQueueRead])
async def get_list_of_queues(
    *,
    session: AsyncSession = Depends(get_async_session),
    nohp: str,
    # idcounter: int,
    date: date,
    statusclient: str,
    statusnumber: str,
):
    queues = await get_queues_by_query_params(
        session=session,
        nohp=nohp,
        date=date,
        statusclient=statusclient,
        statusnumber=statusnumber,
    )
    queues_list: List[Dict[str, any]] = []
    print(queues)
    for queue in queues:
        queues_list.append(transform_queue_data(queue))

    return queues_list
