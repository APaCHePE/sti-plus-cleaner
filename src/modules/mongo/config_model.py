from typing import List, Optional
from pydantic import BaseModel, HttpUrl

class SFTPConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    paths: List[str]

class APIHeader(BaseModel):
    name: str
    value: str

class APIQueryParam(BaseModel):
    name: str
    value: Optional[List[str]]

class ExternalAPIConfig(BaseModel):
    url: HttpUrl
    type: str
    port: Optional[str]
    headers: List[APIHeader]
    query_params: List[APIQueryParam]
    body: Optional[str]

class BucketConfig(BaseModel):
    name: str
    path: str
    entidad: str
    sftp_host: str
    sftp_port: int
    sftp_user: str
    sftp_pass: str
    sftp_path: List[str]
    entidad_externa: str
    sftp_host_externa: str
    sftp_port_externa: int
    sftp_user_externa: str
    sftp_pass_externa: str
    sftp_path_externa: List[str]
    api_url_externo: ExternalAPIConfig
    casilla: str

class ConfigModel(BaseModel):
    _id: dict
    nameBucket: str
    pathBucket: str
    entidadInterna: str
    sftpHostInterna: str
    sftpPortInterna: int
    sftpUserInterna: str
    sftpPassInterna: str
    sftpPathInterna: List[str]
    entidadExterna: str
    sftpHostExterna: str
    sftpPortExterna: int
    sftpUserExterna: str
    sftpPassExterna: str
    sftpPathExterna: List[str]
    apiUrlExterno: ExternalAPIConfig
    casilla: str
