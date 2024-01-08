# services.py
import os
import time
from datetime import datetime
import sys
import tempfile
import uuid
from typing import List

from repositories import UsersRepository
sys.path.append('modules')
from modules.logging.logging_default import logger
from modules.sftp.sftp_read_conn import SftpAmbassadorReadServer, SftpAmbassadorListFilesDetails, SftpAmbassadorListFiles
from modules.storage.storage import upload
from modules.mongo.mongo_conect import Files, ConfigModel, insert, findConfigByCasilla, findFilesByProcessCasillaFolderAndFilenameSizeDateTime
from modules.api_consume.apis import CarpetaInformacionDirectorioDynamic, Prueba, Socket

class UsersService:

    def pruebaSocket():
        ip = "192.168.212.1"
        port = 443
        Socket(ip, port)

    def cleaner(casillaParam, typeConfig) -> List[dict]:
        start_time = time.time()
        codigo_unico = str(uuid.uuid4())
        process = 'CAPTURATOR'
        print(f"CODIGO UNICO -> {codigo_unico}")
        
        # Verifica si existe la casilla en la base de datos
        configsCasilla = findConfigByCasilla(casillaParam, typeConfig)
        if configsCasilla is None:
          print(f"La casilla {casillaParam} no existe en la base de datos")
          return {"status": "ERROR", "message": F"La casilla {casillaParam} no existe en la base de datos", "time": 0}
        print(f"config RESPONSE  1->{configsCasilla}")
        config = ConfigModel(**configsCasilla)
        print(f"config RESPONSE->{config}")  
        ## Crea una única conexión SFTP
        sftp_connection = SftpAmbassadorReadServer(config.sftpUserExterna, config.sftpPassExterna, config.sftpHostExterna, config.sftpPortExterna)
        ## Utiliza la biblioteca magic para obtener el tipo de archivo
        
        listFilesInSFTPByCarpetaCasilla = []
        for param in config.sftpPathExterna:
          print(f"param -> {param}")
          listFolders, listFiles = SftpAmbassadorListFilesDetails(sftp_connection, remote_path=param.path)
          filesByCarpetaCasilla={
            "carpeta": param.carpeta,
            "listFiles": listFiles
          }
          listFilesInSFTPByCarpetaCasilla.append(filesByCarpetaCasilla)
        print(f"listFilesByCarpetoCasilla->{listFilesInSFTPByCarpetaCasilla}")
        
        listaArchivosEnBDPorCasilla = []
        for param in config.sftpPathExterna:
          print(f"param -> {param}")
          listFiles=findFilesByProcessCasillaFolderAndFilenameSizeDateTime(process, casillaParam, param.carpeta)
          print(f"listFiles->{listFiles}")
          filesByCarpetaCasilla={
            "carpeta": param.carpeta,
            "listFiles": listFiles
          }
          listaArchivosEnBDPorCasilla.append(filesByCarpetaCasilla)
        print(f"listaArchivosEnBDPorCasilla->{listaArchivosEnBDPorCasilla}")
        for db_file_carpeta in listFilesInSFTPByCarpetaCasilla:
          # Encontrar la carpeta correspondiente en la lista de archivos del SFTP
          for sftp_file_carpeta in listaArchivosEnBDPorCasilla:
              if db_file_carpeta["carpeta"] == sftp_file_carpeta["carpeta"]:
                # Obtener la lista de archivos del SFTP y de la base de datos
                sftp_file_list = sftp_file_carpeta["listFiles"]
                db_file_list = db_file_carpeta["listFiles"]
                # Filtrar la lista de archivos de la base de datos eliminando los archivos existentes en el SFTP
                db_file_carpeta["listFiles"] = [file for file in db_file_list if file["name"] not in [sftp_file["fileName"] for sftp_file in sftp_file_list]]
        print(f"Final filtered listFilesInSFTPByCarpetaCasilla: {listFilesInSFTPByCarpetaCasilla}")

        
        
        sftp_connection_interna = SftpAmbassadorReadServer(config.sftpUserInterna, config.sftpPassInterna, config.sftpHostInterna, config.sftpPortInterna)
        # ELIMINAR ARCHIVOS 
        UsersService.eliminarArchivosEnServidorBancoRipley(sftp_connection_interna,listFilesInSFTPByCarpetaCasilla)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Tiempo total de ejecución: {elapsed_time} segundos")
        return {"status": "OK", "message": "Se han subido los archivos a Cloud Storage", "time": elapsed_time}
        
        listFilesByCarpetaCasillaInterna = []
        for param in config.sftpPathInterna:
          print(f"param -> {param}")
          # Descarga los archivos de SFTP
          listFolders, listFiles = SftpAmbassadorListFilesDetails(sftp_connection_interna, remote_path=param.path)
          filesByCarpetaCasilla={
            "carpeta": param.carpeta,
            "listFiles": listFiles
          }
          listFilesByCarpetaCasillaInterna.append(filesByCarpetaCasilla)
        # Sube los archivos a Cloud Storage
        print(f"listFilesByCarpetoCasilla->{listFilesByCarpetaCasillaInterna}")
        

        sftp_connection.close()
        sftp_connection_interna.close()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Tiempo total de ejecución: {elapsed_time} segundos")
        return {"status": "OK", "message": "Se han subido los archivos a Cloud Storage", "time": elapsed_time}
      
    def eliminarArchivosEnServidorBancoRipley(sftp_connection_interna, listaDepuradaDeFiles):
      # for carpeta in listFilesByCarpetaCasillaInterna:
      #   for file in carpeta.get('listFiles'):
      #     print(f"Validation carpeta for file -> {file}")
          print(f"PROCESO -> listaDepuradaDeFiles -> {listaDepuradaDeFiles}")
          for carpetaDepurada in listaDepuradaDeFiles:
              for fileDepurado in carpetaDepurada.get('listFiles'):
                  print(f"Eliminando archivo en servidor interno -> {fileDepurado}")
                  try:
                      remote_path = fileDepurado.get('carpeta')
                      filename = fileDepurado.get('name')
                      print(f"Archivo {filename} eliminado en {remote_path}/{filename}")
                      sftp_connection_interna.remove(f"{remote_path}/{filename}")
                  except Exception as e:
                      print(f"No se pudo eliminar {filename} en {remote_path}. Error: {e}")
                  break
              break
          # break
          print({"status": "OK", "message": "Se han eliminado los archivos en el servidor interno"})