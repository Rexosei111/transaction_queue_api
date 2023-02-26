import uvicorn
from database import create_db_tables
from database import drop_db_tables
from fastapi import FastAPI
from namesCounter.router import names_counter_router
from transactionQueue.router import transaction_queue_router

app = FastAPI()
app.include_router(names_counter_router, tags=["Names Counter"])
app.include_router(transaction_queue_router, tags=["Transaction Queue"])


@app.on_event("startup")
async def startup_actions():
    # await drop_db_tables()
    await create_db_tables()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", log_level="info", reload=True)
