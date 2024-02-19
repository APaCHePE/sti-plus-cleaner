from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Union

Base = declarative_base()

class SFTPPath(Base):
    __tablename__ = 'sftp_path'
    id = Column(Integer, primary_key=True, index=True)
    directory = Column(String(255), nullable=False)
    path = Column(String(255), nullable=False)
    process = Column(String(255), nullable=False)
    type_path = Column(String(100))
    config_model_id = Column(Integer, ForeignKey('config_model.id'))
    #config_model = relationship('ConfigModel', back_populates='sftp_paths')
    # Relación para la parte interna
    internal_config_model = relationship('ConfigModel', back_populates='internalSftpPath')

    # Relación para la parte externa
    external_config_model = relationship('ConfigModel', back_populates='externalSftpPath')

class APIQueryParams(Base):
    __tablename__ = 'api_query_params'
    id = Column(Integer, primary_key=True, index=True)
    directory = Column(String, nullable=False)
    process = Column(String, nullable=False)
    params = Column(String, nullable=False)
    config_model_id = Column(Integer, ForeignKey('config_model.id'))
    config_model = relationship('ConfigModel', back_populates='externalApiQueryParams')

class APIHeader(Base):
    __tablename__ = 'api_header'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    value = Column(String, nullable=False)
    config_model_id = Column(Integer, ForeignKey('config_model.id'))
    config_model = relationship('ConfigModel', back_populates='externalApiHeaders')
    
class ConfigModel(Base):
    __tablename__ = 'config_model'
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String, nullable=False)
    bucketName = Column(String, nullable=False)
    bucketPath = Column(String, nullable=False)
    internalEntity = Column(String, nullable=False)
    internalSftpHost = Column(String, nullable=False)
    internalSftpPort = Column(Integer, nullable=False)
    internalSftpUser = Column(String, nullable=False)
    internalSftpPassword = Column(String, nullable=False)
    #internalSftpPath = relationship('SFTPPath', back_populates='config_model', cascade='all, delete-orphan')
    externalEntity = Column(String, nullable=False)
    externalSftpHost = Column(String, nullable=False)
    externalSftpPort = Column(Integer, nullable=False)
    externalSftpUser = Column(String, nullable=False)
    externalSftpPassword = Column(String, nullable=False)
    #externalSftpPath = relationship('SFTPPath', back_populates='config_model', cascade='all, delete-orphan')
    externalApiUrl = Column(String, nullable=False)
    externalApiType = Column(String, nullable=False)
    externalApiPort = Column(String, nullable=False)
    externalApiHeaders = relationship('APIHeader', back_populates='config_model', cascade='all, delete-orphan')
    externalApiQueryParams = relationship('APIQueryParams', back_populates='config_model', cascade='all, delete-orphan')
    # externalApiQueryParams = relationship('APIQueryParamsExterno', back_populates='config_model', cascade='all, delete-orphan')
    externalApiBody = Column(Text, nullable=True)
    
    #api_header = relationship('APIHeader', back_populates='config_model')
    #sftp_paths = relationship('SFTPPath', back_populates='config_model', cascade='all, delete-orphan')
    
    internalSftpPath = relationship('SFTPPath', back_populates='internal_config_model', cascade='all, delete-orphan', overlaps='internal_config_model', primaryjoin='and_(ConfigModel.id == SFTPPath.config_model_id, SFTPPath.type_path == "INTERNAL")')
    
    externalSftpPath = relationship('SFTPPath', back_populates='external_config_model', cascade='all, delete-orphan', overlaps='external_config_model', primaryjoin='and_(ConfigModel.id == SFTPPath.config_model_id, SFTPPath.type_path == "EXTERNAL")')
