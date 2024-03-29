# services.py
import os
import time
from datetime import datetime
import sys
import tempfile
import uuid
from typing import List

sys.path.append('modules')
from modules.logging.logging_default import logger
from modules.sftp.sftp_read_conn import SftpAmbassadorReadServer, SftpAmbassadorListFilesDetails, SftpAmbassadorListFiles
from modules.storage.storage import upload
from modules.api_consume.apis import CarpetaInformacionDirectorioDynamic, Prueba, Socket
from modules.mysql.mysqlconect import findConfigByCasillaMysql, findFilesByStatusAndProcessMysql, updateMysql
from modules.mysql.modelfile import File

class UsersService:

    def cleaner(user, process) -> List[dict]:
        start_time = time.time()
        codigo_unico = str(uuid.uuid4())
        statusFilesDeleted = "COMPLETE"
        print(f"CODIGO UNICO -> {codigo_unico}")
        try:
          # Verifica si existe la casilla en la base de datos
          config = findConfigByCasillaMysql(user, statusFilesDeleted)
          # for pathExternal in config.externalSftpPath:
          #     print(f"Path: {pathExternal.directory} -> {pathExternal.path} -> {pathExternal.process} -> {pathExternal.type_path}")
          
          with SftpAmbassadorReadServer(config.externalSftpUser, config.externalSftpPassword, config.externalSftpHost, config.externalSftpPort) as sftp_connection:
            ## Utiliza la biblioteca magic para obtener el tipo de archivo
            listFilesInSFTPByCarpetaCasilla = [
              {"carpeta": param.directory, "listFiles": listFiles}
              for param in config.externalSftpPath
              if (listFiles := SftpAmbassadorListFilesDetails(sftp_connection, remote_path=param.path))
            ]
            print(f"listFilesByCarpetaCasilla | listFiles | ->{listFilesInSFTPByCarpetaCasilla}")
            
            listaArchivosEnBDPorCasilla = [
              {"carpeta": param.directory, "listFiles": listFiles}
              for param in config.externalSftpPath
              if (listFiles := findFilesByStatusAndProcessMysql("COMPLETE", user, param.directory))
            ]
            print(f"listaArchivosEnBDPorCasilla | listFiles | ->{listaArchivosEnBDPorCasilla}")
            
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
            # for sftp_file_carpeta in listFilesInSFTPByCarpetaCasilla:
            #     for db_file_carpeta in listaArchivosEnBDPorCasilla:
            #         if db_file_carpeta["carpeta"] == sftp_file_carpeta["carpeta"]:
            #             db_files = db_file_carpeta["listFiles"]
            #             sftp_files = sftp_file_carpeta["listFiles"]
            #             print(f"db_files->{db_files}")
            #             print(f"sftp_files->{sftp_files}")
            #             try:
            #                 list_files = []
            #                 for db_file in db_files:
            #                     print(f"db_file->{db_file['fileName']}")
            #                     for sftp_file in sftp_files:
            #                         print(f"sftp_file->{sftp_file['name']}")
            #                         if db_file["fileName"] != sftp_file["name"]:
            #                             # print(f"FileName: {db_file.get("fileName")} | Name: {sftp_file.name}")
            #                             list_files.append(db_file)
            #                 print(f"directory->{db_file_carpeta['carpeta']}|list_files->{list_files}")
            #                 db_file_carpeta["listFiles"] = list_files
            #                 # db_file_carpeta["listFiles"] = [db_file for db_file in db_files if db_file["fileName"] not in [sftp_file["name"] for sftp_file in sftp_files]]
            #                 # db_file_carpeta["listFiles"] = [file for file in db_files if file["fileName"] not in [sftp_file["name"] for sftp_file in sftp_files]]
            #                 # db_file_carpeta["listFiles"] = [db_file for db_file in d.b_files if db_file["fileName"] not in [sftp_file["name"] for sftp_file in sftp_files]]
            #             except Exception as e:
            #                 print(f"Error al filtrar archivos: {e}")
            #             #db_file_carpeta["listFiles"] = [db_file for db_file in db_files if db_file["fileName"] not in [sftp_file["name"] for sftp_file in sftp_files]]
            #             result.append(db_file_carpeta)
            #             break
            # Iterar sobre cada carpeta en listFilesByCarpetaCasilla
            for carpeta_bd in listaArchivosEnBDPorCasilla:
                # Obtener la lista de archivos para esta carpeta
                archivos_carpeta_bd = carpeta_bd['listFiles']
                
                # Obtener la carpeta correspondiente en listaArchivosEnBDPorCasilla
                for carpeta in listFilesInSFTPByCarpetaCasilla:
                    if carpeta['carpeta'] == carpeta_bd['carpeta']:
                        archivos_sftp = carpeta['listFiles']
                        break
                
                # Verificar cada archivo en la carpeta actual
                for archivo_bd in archivos_carpeta_bd:
                    nombre_archivo = archivo_bd['fileName']
                    
                    # Verificar si el nombre del archivo existe en la lista de archivos de listaArchivosEnBDPorCasilla
                    encontrado = False
                    for archivo_sftp in archivos_sftp:
                        if archivo_sftp['name'] == nombre_archivo:
                            encontrado = True
                            break
                    
                    # Si el archivo no se encuentra en la lista de archivos de listaArchivosEnBDPorCasilla, agregarlo a la lista de resultados
                    if not encontrado:
                        result.append(archivo_bd)
            print(f"Final filtered result: {result}")
            for res in result:
              print(f"RESSSSSULT >>>>{res} ")
            with SftpAmbassadorReadServer(config.internalSftpUser, config.internalSftpPassword, config.internalSftpHost, config.internalSftpPort) as sftp_connection_interna:
            
              # ELIMINAR ARCHIVOS 
              listaFInalDeArchivosEliminadosPorCarpeta = []
              for param in config.internalSftpPath:
                print(f"param deletes -> {param}")
                listFilesEliminados = UsersService.eliminarArchivosEnServidorBancoRipley(sftp_connection_interna, param, result)
                print(f"return LIST ARCHIVOS {listFilesEliminados}")
                filesByCarpetaCasilla={
                  "carpeta": param.directory,
                  "listFiles": listFilesEliminados
                }
                listaFInalDeArchivosEliminadosPorCarpeta.append(filesByCarpetaCasilla)
              
              print(f"listaFInalDeArchivosEliminadosPorCarpeta->{listaFInalDeArchivosEliminadosPorCarpeta}")
              
              for file in listaFInalDeArchivosEliminadosPorCarpeta:
                file['idProcessDelete'] = f"{codigo_unico}"
                print(f"listaFInalDeArchivosEliminadosPorCarpeta file-> {file}")
                if len(file.listFiles) > 0: 
                  UsersService.updateFilesInBD(file.listFiles)

          return {"status": "OK", "message": "Se han subido los archivos a Cloud Storage", "time": elapsed_time}
        except Exception as e:
            print(f"Error inesperado: {e}")
            #return {"status": "ERROR", "message": "Ocurrió un error inesperado", "time": 0}
        finally:
            elapsed_time = time.time() - start_time
            print(f"Tiempo total de ejecución: {elapsed_time} segundos del proceso:{codigo_unico}")
      
    def eliminarArchivosEnServidorBancoRipley(sftp_connection_interna, sftp, listaDepuradaDeFiles):
      # for carpeta in listFilesByCarpetaCasillaInterna:
      #   for file in carpeta.get('listFiles'):
      #     print(f"Validation carpeta for file -> {file}")
      listArchivoEliminador = []
      print(f"PROCESO -> listaDepuradaDeFiles -> {listaDepuradaDeFiles}")
      for carpetaDepurada in listaDepuradaDeFiles:
          print(f"PROCESO_2 -> carpetaDepurada -> {carpetaDepurada}")
          if carpetaDepurada.get('directory') == sftp.directory:
            print(f"PROCESO_3 -> sftp.carpeta -> {sftp.directory}")
            print(f"file depurado {carpetaDepurada.get('listFiles')}")
            # for fileDepurado in carpetaDepurada.get('listFiles'):
            #     print(f"Eliminando archivo en servidor interno -> {fileDepurado}")
            try:
                    # Verificar si el archivo existe
              remote_path = sftp.path
              fileName = carpetaDepurada.get('fileName')
              sftp_connection_interna.stat(f"{remote_path}/{fileName}")
              print(f"El archivo {fileName} existe en {remote_path}")
              print(f"Archivo {fileName} eliminado en {remote_path}/{fileName}")
              sftp_connection_interna.remove(f"{remote_path}/{fileName}")
              listArchivoEliminador.append(carpetaDepurada)
              print({"status": "OK", "message": "Se han eliminado el archivo en el servidor interno "})
            except Exception as e:
                print(f"ERROR: No se pudo eliminar {fileName} en {remote_path}. Error: {e}")
                    
      return listArchivoEliminador
    
    def updateFilesInBD(file): 
      file["statusFile"] = 'ELIMINADO'
      updateMysql(file.get("idFile"), file)
    