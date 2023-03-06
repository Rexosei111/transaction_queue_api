from datetime import datetime

from database import Base
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import relationship


class TransactionQueue(Base):
    __tablename__ = "ttransaksiqueue"
    idqueue = Column(Integer, primary_key=True)
    idcounter = Column(Integer, ForeignKey("tnamescounter.idcounter"))
    tnamecounter = relationship("TNamesCounter", back_populates="transactionqueues")
    nohpclient = Column(String, nullable=False)
    statusclient = Column(String(20), default=None)
    statusnumber = Column(String(20), default=None)
    yournumber = Column(Integer, nullable=False)
    timestamp = Column(TIMESTAMP, default=datetime.now())
    date = Column(Date, default=datetime.date(datetime.now()))
