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
from .services import get_queues_count_by_date
from .services import get_queues_count_by_idcounter_and_date
from .services import get_queues_count_by_statusnumber
from .services import update_queue

transaction_queue_router = APIRouter(prefix="/api/v1/queues")


def transform_queue_data(queue: TransactionQueue):
    queue_dict = queue.__dict__
    tnamecounter: TNamesCounter = queue_dict.pop("tnamecounter")  # type: ignore
    tnamecounter: Dict[str, any] = tnamecounter.__dict__
    queue_dict = {**queue_dict, **tnamecounter}
    return queue_dict


@transaction_queue_router.post(
    "/",
    response_model=TransactionQueueRead,
    response_class=CustomResponse,
    status_code=200,
)
async def add_queue(
    data: TransactionQueueCreate,
    session: AsyncSession = Depends(get_async_session),
):
    queue = await create_queue(session, data)
    queues_count = await get_queues_count_by_statusnumber(
        session, idcounter=data.idcounter, date=data.date
    )  # type: ignore
    queues_count_by_idcounter_and_date = await get_queues_count_by_idcounter_and_date(
        session, idcounter=data.idcounter, date=data.date
    )
    queue_dict = {
        **transform_queue_data(queue),
        "endnumber": queues_count_by_idcounter_and_date,
        "posnumber": queues_count,
    }

    return queue_dict


@transaction_queue_router.put(
    "/", response_model=TransactionQueueRead, response_class=CustomResponse
)
async def edit_queue(
    *,
    session: AsyncSession = Depends(get_async_session),
    data: TransactionQueueUpdate,
    current_name_counter=Depends(get_current_name_counter),
):
    queue = await update_queue(session, data, current_name_counter=current_name_counter)
    queues_count = await get_queues_count_by_statusnumber(
        session, idcounter=data.idcounter, date=data.date
    )
    queues_count_by_idcounter_and_date = await get_queues_count_by_idcounter_and_date(
        session, idcounter=data.idcounter, date=queue.date
    )
    queue_dict = {
        **transform_queue_data(queue),
        "endnumber": queues_count_by_idcounter_and_date,
        "posnumber": queues_count,
    }
    return queue_dict


@transaction_queue_router.get("/", response_model=List[TransactionQueueRead])
async def get_list_of_queues(
    *,
    session: AsyncSession = Depends(get_async_session),
    idcounter: int,
    date: date,
    statusclient: str = "",
    statusnumber: str = "",
):
    queues = await get_queues_by_query_params(
        session=session,
        idcounter=idcounter,
        date=date,
        statusclient=statusclient,
        statusnumber=statusnumber,
    )
    queues_count = await get_queues_count_by_statusnumber(
        session, idcounter=idcounter, date=date
    )
    endnumber = await get_queues_count_by_idcounter_and_date(
        session, idcounter=idcounter, date=date
    )
    queues_dict: List[Dict[str, any]] = []
    for queue in queues:
        queues_dict.append(
            {
                **transform_queue_data(queue),
                "endnumber": endnumber,
                "posnumber": queues_count,
            }
        )

    return queues_dict
