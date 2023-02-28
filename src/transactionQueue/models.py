from datetime import datetime

from database import Base
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Sequence
from sqlalchemy import String
from sqlalchemy import Time
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import relationship


class TransactionQueue(Base):
    __tablename__ = "ttransaksiqueue"
    number_sec = Sequence(__tablename__ + "__id_seq")
    idqueue = Column(Integer, primary_key=True)
    idcounter = Column(Integer, ForeignKey("tnamescounter.idcounter"))
    tnamecounter = relationship("TNamesCounter", back_populates="transactionqueues")
    statusclient = Column(String(20), default=None)
    statusnumber = Column(String(20), default=None)
    yournumber = Column(
        Integer, number_sec, server_default=number_sec.next_value(), nullable=False
    )
    timestamp = Column(TIMESTAMP, default=datetime.time(datetime.now()))
    date = Column(Date, default=datetime.date(datetime.now()))
