from datetime import datetime

from database import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Time
from sqlalchemy.orm import relationship


class TNamesCounter(Base):
    __tablename__ = "tnamescounter"

    idcounter = Column(Integer, primary_key=True)
    namecounter = Column(String, nullable=False)
    address = Column(String)
    nohp = Column(String, unique=True, nullable=False)
    otp = Column(String, unique=True, nullable=False)
    location = Column(String)
    timeclosing = Column(Time, default=datetime.time(datetime.now()))
    transactionqueues = relationship(
        "TransactionQueue", back_populates="tnamecounter", cascade="all, delete-orphan"
    )
