import uvicorn
from database import create_db_tables
from database import drop_db_tables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from namesCounter.router import names_counter_router
from transactionQueue.router import transaction_queue_router

app = FastAPI(title="Transaction Queue API")
app.include_router(names_counter_router, tags=["Names Counter"])
app.include_router(transaction_queue_router, tags=["Transaction Queue"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_actions():
    # await drop_db_tables()
    await create_db_tables()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", log_level="info", reload=True)
