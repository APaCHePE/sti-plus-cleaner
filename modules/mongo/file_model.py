from pydantic import BaseModel
from typing import List

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