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
from modules.mongo.mongo_conect import Files, ConfigModel, update, findConfigByCasilla, findFilesByProcessCasillaFolderAndFilenameSizeDateTime
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
          filesByCarpetaCasilla={
            "carpeta": param.carpeta,
            "listFiles": listFiles
          }
          listaArchivosEnBDPorCasilla.append(filesByCarpetaCasilla)
        print(f"listaArchivosEnBDPorCasilla->{listaArchivosEnBDPorCasilla}")
        
        '''listFilesInSFTPByCarpetaCasillaInterna = []
        for param in config.sftpPathInterna:
          print(f"param -> {param}")
          # Descarga los archivos de SFTP
          listFolders, listFiles = SftpAmbassadorListFilesDetails(sftp_connection_interna, remote_path=param.path)
          filesByCarpetaCasilla={
            "carpeta": param.carpeta,
            "listFiles": listFiles
          }
          listFilesInSFTPByCarpetaCasillaInterna.append(filesByCarpetaCasilla)
        # Sube los archivos a Cloud Storage
        print(f"listFilesByCarpetoCasilla->{listFilesInSFTPByCarpetaCasillaInterna}")'''
        
        result = []
        for sftp_file_carpeta in listFilesInSFTPByCarpetaCasilla:
            for db_file_carpeta in listaArchivosEnBDPorCasilla:
                if db_file_carpeta["carpeta"] == sftp_file_carpeta["carpeta"]:
                    db_files = db_file_carpeta["listFiles"]
                    sftp_files = sftp_file_carpeta["listFiles"]
                    db_file_carpeta["listFiles"] = [db_file for db_file in db_files if db_file["fileName"] not in [sftp_file["name"] for sftp_file in sftp_files]]
                    result.append(db_file_carpeta)
                    break
                  
        print(f"Final filtered result: {result}")
        
        sftp_connection_interna = SftpAmbassadorReadServer(config.sftpUserInterna, config.sftpPassInterna, config.sftpHostInterna, config.sftpPortInterna)
        # ELIMINAR ARCHIVOS 
        
        listaFInalDeArchivosEliminadosPorCarpeta = []
        for param in config.sftpPathInterna:
          print(f"param deletes -> {param}")
          listFilesEliminados = UsersService.eliminarArchivosEnServidorBancoRipley(sftp_connection_interna, param, result)
          filesByCarpetaCasilla={
            "carpeta": param.carpeta,
            "listFiles": listFilesEliminados
          }
          listaFInalDeArchivosEliminadosPorCarpeta.append(filesByCarpetaCasilla)
        
        print(f"listaFInalDeArchivosEliminadosPorCarpeta->{listaFInalDeArchivosEliminadosPorCarpeta}")
        
        for file in listaFInalDeArchivosEliminadosPorCarpeta:
          if len(file.listFiles) > 0: 
            UsersService.updateFilesInBD(file.listFiles)
        
        sftp_connection.close()
        sftp_connection_interna.close()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Tiempo total de ejecución: {elapsed_time} segundos")
        return {"status": "OK", "message": "Se han subido los archivos a Cloud Storage", "time": elapsed_time}
      
    def eliminarArchivosEnServidorBancoRipley(sftp_connection_interna, sftp, listaDepuradaDeFiles):
      # for carpeta in listFilesByCarpetaCasillaInterna:
      #   for file in carpeta.get('listFiles'):
      #     print(f"Validation carpeta for file -> {file}")
      listArchivoEliminador = []
      print(f"PROCESO -> listaDepuradaDeFiles -> {listaDepuradaDeFiles}")
      for carpetaDepurada in listaDepuradaDeFiles:
          print(f"PROCESO_2 -> carpetaDepurada -> {carpetaDepurada}")
          if carpetaDepurada.get('carpeta') == sftp.carpeta:
            print(f"PROCESO_3 -> sftp.carpeta -> {sftp.carpeta}")
            for fileDepurado in carpetaDepurada.get('listFiles'):
                print(f"Eliminando archivo en servidor interno -> {fileDepurado}")
                try:
                    # Verificar si el archivo existe
                    remote_path = sftp.path
                    filename = fileDepurado.get('fileName')
                    sftp_connection_interna.stat(f"{remote_path}/{filename}")
                    print(f"El archivo {filename} existe en {remote_path}")
                    print(f"Archivo {filename} eliminado en {remote_path}/{filename}")
                    sftp_connection_interna.remove(f"{remote_path}/{filename}")
                    listArchivoEliminador.append(fileDepurado)
                    print({"status": "OK", "message": "Se han eliminado el archivo en el servidor interno "})
                except Exception as e:
                    print(f"ERROR: No se pudo eliminar {filename} en {remote_path}. Error: {e}")
                    
      return listArchivoEliminador
    
    def updateFilesInBD(file): 
      file["statusFile"] = 'ELIMINADO'
      update(file.get("_id"),file)
    