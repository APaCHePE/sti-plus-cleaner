from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class File(Base):
    __tablename__ = 'files'

    idFile = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(String(255))
    executionDate = Column(DateTime, default=datetime.utcnow)
    typeProcess = Column(String(255))
    idProcessGet = Column(String(36))
    idProcessPut = Column(String(36))
    idProcessDelete = Column(String(36))
    runtimeGet = Column(Float)
    runtimePut = Column(Float)
    runtimeDelete = Column(Float)
    directory = Column(String(255))
    fileName = Column(String(255))
    type = Column(String(255))
    size = Column(Integer)
    date = Column(String(10))
    time = Column(String(8))
    bucketName = Column(String(255))
    bucketPath = Column(String(255))
    statusFile = Column(String(255))
    
    def __repr__(self):
        return f"<File(idFile={self.idFile}, fileName={self.fileName}, user={self.user})>"
