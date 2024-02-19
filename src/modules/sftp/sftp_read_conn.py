import os
import pysftp
import time
import datetime
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

load_dotenv()

class SftpConnectionManager:
    def __init__(self):
        print("abriendo conexión")
        self.sftp = None

    def __enter__(self):
        # Aquí configuras y devuelves la conexión SFTP
        SFTP_HOST = '35.208.24.22'
        SFTP_USER = 'sti-plus-developer'
        SFTP_PASS = "uZ_W#7nwUPZk0lj"
        SFTP_PORT = int(22)
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        self.sftp = pysftp.Connection(host=SFTP_HOST, username=SFTP_USER, password=SFTP_PASS, port=SFTP_PORT, cnopts=cnopts)
        return self.sftp

    def __exit__(self, exc_type, exc_value, traceback):
        print("Cerrando conexión")
        # Cierras la conexión SFTP
        if self.sftp:
            self.sftp.close()


def SftpAmbassadorReadServer(userSftp, passSftp, hostSftp, portSftp):
    # Reading environment variables
    print("------------------------ CONECT SERVER --------------------")
    print(f"SFTP_HOST->{hostSftp}|SFTP_USER->{userSftp}|SFTP_PASS->{passSftp}SFTP_PORT->{portSftp}")
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None  # Disable host key checking; not recommended for production
    try:
      sftp = pysftp.Connection(host=hostSftp, username=userSftp, password=passSftp, port=int(portSftp), cnopts=cnopts)
      print("Conexión establecida")
      return sftp

    except Exception as e:
        print(f"connect_server error occurred: {e}")

def SftpAmbassadorGetFile(sftp : pysftp.Connection, local_path, remote_path, filename):
    print("invocando funcion SftpAmbassadorGetFile")
    try:
        sftp.get(os.path.join(remote_path, filename), localpath = local_path+"/"+filename, preserve_mtime=True)
    except Exception as e:
        print(f"SftpAmbassadorGetFile error occurred: {e}")


def SftpAmbassadorTransport(sftp : pysftp.Connection, local_path, remote_path, filename):
    print("invocando funcion SftpAmbassadorTransport")
    try:
        sftp.put(local_path+"/"+ filename, remotepath = remote_path+"/"+filename, preserve_mtime=True)
    except Exception as e:
        print(f"SftpAmbassadorTransport error occurred: {e}")
    
def SftpAmbassadorTransportByFilename(sftp: pysftp.Connection, contents, remote_path, filename):
    start_time1 = time.time() 
    for i in range(3):
        print(f"Intento {i+1} de 3")
        try:            
            with sftp.open(remote_path + "/" + filename, "wb") as file:
                file.write(contents)
            end_time1 = time.time()  # Guarda el tiempo de finalización
            elapsed_time1 = end_time1 - start_time1  # Calcula el tiempo transcurrido
            print(f"{filename} demoró {elapsed_time1} segundos")
            break
        except Exception as e:
            print(f"Error al transferir archivo: {e}")
            time.sleep(5)
            
def SftpAmbassadorTransportByFilenameHilos(sftp: pysftp.Connection, contents, remote_path, filename):
    start_time1 = time.time()

    # Divide el archivo en bloques de 16384 bytes
    blocks = contents.split(b"\n", 8192)

    # Transfere los bloques simultáneamente
    with sftp.open(remote_path + "/" + filename, "wb") as file:
        with ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(lambda block: file.write(block), blocks)

    end_time1 = time.time()
    elapsed_time1 = end_time1 - start_time1
    print(f"{filename} demoró {elapsed_time1} segundos")
    
def SftpAmbassadorListFiles(sftp: pysftp.Connection, remote_path):
    print("invocando funcion SftpAmbassadorListFiles")
    try:
        # Obtener la ruta de trabajo actual 
        print(f"Ruta de trabajo actual: {remote_path}")
        remote_path = f"/cas_05/sat/ripley/ripprod/dat/despat01{remote_path}"
        file_list = sftp.listdir(f"/cas_05/sat/ripley/ripprod/dat/despat01{remote_path}")
        print(f"file_list: {file_list}")
        folders = [item for item in file_list if sftp.isdir(remote_path + '/' + item)]
        files = [item for item in file_list if sftp.isfile(remote_path + '/' + item)]
        return folders, files
    except Exception as e:
        print(f"SftpAmbassadorListFiles error occurred: {e}")
        return [], []

def SftpAmbassadorListFilesDetails(sftp: pysftp.Connection, remote_path):
    print("invocando funcion SftpAmbassadorListFilesDetails")
    try:
        # print(f"Ruta de trabajo actual: {remote_path}")
        # remote_path = f"/cas_05/sat/ripley/ripprod/dat/despat01{remote_path}"
        print(f"Ruta de trabajo actual: {remote_path}")
        
        file_info_list = []
        print(f"Ruta de trabajo actual: {sftp.listdir(remote_path)}")
        for item in sftp.listdir(remote_path):
            item_path = f"{remote_path}/{item}"
            is_dir = sftp.isdir(item_path)
            file_info = {"name": item,"is_dir": is_dir}
            if not is_dir:
                # Obtener información adicional para archivos no directorios
                stat_result = sftp.stat(item_path)
                file_info["size"] = stat_result.st_size
                file_info["date"] = datetime.datetime.fromtimestamp(stat_result.st_mtime).strftime('%Y-%m-%d')
                file_info["time"] = datetime.datetime.fromtimestamp(stat_result.st_mtime).strftime('%H:%M:%S')
            file_info_list.append(file_info)
        files = [item for item in file_info_list if not item["is_dir"]]

        if not files:
            raise NoFilesFoundError("No se encontraron archivos en el directorio especificado.")

        print(f"Archivos encontrados: {files}")
        return files

    except Exception as e:
        print(f"SftpAmbassadorListFilesDetails error occurred: {e}")

class NoFilesFoundError(Exception):
    pass