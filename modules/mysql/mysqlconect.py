from sqlalchemy import create_engine, Column, String, DateTime, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.exc import NoResultFound
from .modelconfig import ConfigModel
from .modelfile import File

Base = declarative_base()

# Configurar la conexión a la base de datos MySQL
DATABASE_URL = "mysql+mysqlconnector://root:@35.236.216.155/stiplus"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

# Crear una sesión de SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()

def findFilesByStatusAndProcessMysql(status, typeProcess):
    try:
        print("STATUS: " + status + " TYPE: " + typeProcess)
        result = session.query(File).filter_by(statusFile=status, typeProcess=typeProcess).all()
        print("Found files:", result)
        if len(result) == 0:
            print("No files found")
            return None
        return [file.__dict__ for file in result]
    except FileNotFoundError as e:
        # Manejo genérico de excepciones, puedes personalizarlo según tus necesidades.
        print(f"Error al buscar archivos: {e}")
        return None
    finally:
        session.close()

def findFilesByDirectoryFilenameSizeDateTimeMysql(user, directory):
    try:
        print(f"[findFilesByDirectoryFilenameSizeDateTimeMysql] [INIT]|{user}|{directory}")
        result = session.query(File).filter_by(
            user=user,
            directory=directory
        ).first()
        if result is None:
            raise FileNotFoundError("No se encontró archivo para el usuario")
        print("[findFilesByDirectoryFilenameSizeDateTimeMysql] [FIN]",result.__dict__)
        return result.__dict__
    except FileNotFoundError as e:
        # Manejo genérico de excepciones, puedes personalizarlo según tus necesidades.
        print(f"FileNotFoundError: {e}")
        return None
    finally:
        session.close()
        
def findConfigByCasillaMysql(user: str) -> ConfigModel:
    try:
        print("User:", user)
        result = session.query(ConfigModel).filter_by(user=user).one()
        # Obtener el diccionario de atributos del objeto ConfigModel
        api_headers = result.externalApiHeaders
        # Iterar sobre la lista de APIHeader
        for api_header in api_headers:
            print("API HEADER", api_header.name, api_header.value)

        api_query_params = result.externalApiQueryParams
        # Iterar sobre la lista de APIHeader
        for api_header in api_query_params:
            print("API PARAMS", api_header.process, api_header.directory, api_header.params)
            
        externalSftpPath = result.externalSftpPath
        internalSftpPath = result.internalSftpPath
        # Iterar sobre la lista de APIHeader
        for ext_api_paths in externalSftpPath:
            print("API PATHS", ext_api_paths.directory, ext_api_paths.path, ext_api_paths.process, ext_api_paths.type_path)
        for int_api_paths in internalSftpPath:
            print("API PATHS", int_api_paths.directory, int_api_paths.path, int_api_paths.process, int_api_paths.type_path)
            
        
        config_dict = result.__dict__
        # Eliminar atributos especiales y solo dejar los atributos que necesitas
        config_dict = {key: value for key, value in config_dict.items() if not key.startswith('_')}

        print(f"Configuracion de la casilla {user} -> {config_dict}")
        return result
    except NoResultFound:
        raise ConfigNotFoundException(f"No se encontró configuración para el usuario {user}")
    finally:
        session.close()

def insertMysql(item: File):
    # Crear una instancia del modelo File
    '''file_instance = File(
        user=item.user,
        typeProcess=item.typeProcess,
        directory=item.directory,
        fileName=item.fileName,
        size=item.size,
        date=item.date,
        time=item.time,
        bucketName=item.bucketName,
        executionDate=datetime.now(),
        idProcessGet=item.idProcessGet,
        runtimeGet=item.runtimeGet,
        type=item.type,
        bucketPath=item.bucketPath,
        statusFile=item.statusFile
    )'''
    print("INSET MYSQL", item)
    # Agregar la instancia a la sesión y hacer commit
    session.add(item)
    session.commit()

    return item.idFile

class ConfigNotFoundException(Exception):
    pass

def updateMysql(item_id: int, updated_data: dict):
    try:
        # Elimina la clave '_sa_instance_state' si está presente
        updated_data.pop('_sa_instance_state', None)
        
        # Realiza la actualización en MySQL
        print("UPDATE MYSQL", item_id, updated_data)
        stmt = update(File).where(File.idFile == item_id).values(updated_data)
        
        session.execute(stmt)
        session.commit()
        # Recupera y retorna el objeto actualizado
        updated_item = session.query(File).filter_by(idFile=item_id).first()
        return updated_item
    except Exception as e:
        print(f"Error al actualizar en MySQL: {e}")
        session.rollback()
        return None
    finally:
        session.close()