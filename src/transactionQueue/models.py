from datetime import datetime

from database import Base
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Time
from sqlalchemy.orm import relationship


class TransactionQueue(Base):
    __tablename__ = "ttransaksiqueue"
    idqueue = Column(Integer, primary_key=True)
    idcounter = Column(Integer, ForeignKey("tnamescounter.idcounter"))
    tnamecounter = relationship("TNamesCounter", back_populates="transactionqueues")
    statusclient = Column(String(20))
    statusnumber = Column(String(20))
    yournumber = Column(Integer)
    positionnumber = Column(Integer)
    endnumber = Column(Integer)
    timestamp = Column(Time, default=datetime.time(datetime.now()))
    date = Column(Date, default=datetime.date(datetime.now()))
