from os import environ as env 
from bson import ObjectId
from pymongo import MongoClient
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Union
    
class Files(BaseModel):
  idProceso: str
  fechaHoraProceso: str
  tipoProceso: str
  casilla: str
  tiempoEjecucionGet: float
  tiempoEjecucionPut: float
  carpeta: str
  fileName: str
  type: str
  size: str
  date: str
  time: str
  nombreBucket: str
  nombreCarpeta: str
  statusFile: str
  casilla: str
# Conectarse a MongoDB
client = MongoClient('mongodb+srv://sti-plus-developer:1Z9kQdtrwR5ZGodB@sti-plus-cluster-01.1vjognq.mongodb.net/')

# Seleccionar una base de datos
db = client['ripley-stiplus']
# Seleccionar una colección
collectionProcess = db['liberator']
config = db['configuracion']

def insert(item: Files):
  item_dict = item.dict()
  result = collectionProcess.insert_one(item_dict)
  return result.inserted_id

def findFilesByProcessCasillaFolderAndFilenameSizeDateTime(process: str, casilla: str, folder: str):
  print(f"process->{process}|casilla->{casilla}|carpeta->{folder}")
  results = collectionProcess.find({"tipoProceso": "LIBERADOR", "casilla": "FISA_TATA_CANJE", "carpeta": folder, "statusFile": {"$ne": "ELIMINADO"} })
  return list(results)  # Convertimos el cursor a una lista de documentos
  
def findConfigByCasilla(casilla: str, typeConfig: str):
  print(f"config->{config}|casilla->{casilla}|typeConfig->{typeConfig}")
  result = config.find_one({"casilla": casilla, "config":typeConfig})
  if result is None:
    return False
  return result

def find(item_id):
  object_id = ObjectId(item_id)
  result = collectionProcess.find_one({"_id": object_id})
  print(result)
  if result:
    # Convertir el ObjectId a str antes de retornar la respuesta
    result["_id"] = str(result["_id"])
    return result

def update(item_id: str, item: Files):
  object_id = ObjectId(item_id)
  item_dict = item.dict()
  result = collectionProcess.find_one_and_update(
    {"_id": object_id},
    {"$set": item_dict},
    return_document=True
  )
  print(result)
  if result:
    result["_id"] = str(result["_id"])
    return result
  
class SFTPPath(BaseModel):
    carpeta: str
    path: str

class APIHeader(BaseModel):
    name: str
    value: str

class APIQueryParam(BaseModel):
    name: str
    value: Optional[Union[str, List[str]]]

class APIQueryParamsExterno(BaseModel):
    carpeta: str
    params: List[APIQueryParam]
class ConfigModel(BaseModel):
    nameBucket: str
    pathBucket: str
    entidadInterna: str
    sftpHostInterna: str
    sftpPortInterna: int
    sftpUserInterna: str
    sftpPassInterna: str
    sftpPathInterna: List[SFTPPath]
    entidadExterna: str
    sftpHostExterna: str
    sftpPortExterna: int
    sftpUserExterna: str
    sftpPassExterna: str
    sftpPathExterna: List[SFTPPath]
    apiUrlExterno: HttpUrl
    apiTipoExterno: str
    apiPortExterno: str
    apiHeadersExterno: List[APIHeader]
    apiQueryParamsExterno: List[APIQueryParamsExterno]
    apiBodyExterno: Optional[str]
    casilla: str
    config: str