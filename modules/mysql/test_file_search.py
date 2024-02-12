import unittest
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from mysqlconect import findFilesByProcessUserDirectoryFilenameSizeDateTime

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
    size = Column(String(255))
    date = Column(String(10))
    time = Column(String(8))
    bucketName = Column(String(255))
    bucketPath = Column(String(255))
    statusFile = Column(String(255))

# Configurar la conexión a la base de datos MySQL para pruebas
TEST_DATABASE_URL = "mysql+mysqlconnector://root@35.236.216.155/stiplus"
test_engine = create_engine(TEST_DATABASE_URL)
Base.metadata.create_all(bind=test_engine)

class TestFileSearch(unittest.TestCase):

    def setUp(self):
        # Configurar la sesión de SQLAlchemy para pruebas
        print("INICIANDO SETUP TEST")
        Session = sessionmaker(bind=test_engine)
        self.session = Session()

        # Insertar datos de prueba en la tabla files
        test_file = File(
            user='CREASYS',
            typeProcess='LIBERATOR',
            directory='salida',
            fileName='liberator-ripley_2.pdf',
            size='31859',
            date='2023-09-22',
            time='16:52:40'
        )
        self.session.add(test_file)
        self.session.commit()

    def tearDown(self):
        # Limpiar solo los datos insertados después de cada prueba
        Base.metadata.drop_all(bind=test_engine)
        print("Tear down")

    def test_findFilesByProcessUserDirectoryFilenameSizeDateTime(self):
        # Prueba de búsqueda exitosa
        result = findFilesByProcessUserDirectoryFilenameSizeDateTime(
            typeProcess='LIBERATOR',
            user='CREASYS',
            directory='salida',
            fileName='liberator-ripley_2.pdf',
            size='31859',
            date='2023-09-22',
            time='16:52:40'
        )
        self.assertIsNotNone(result)
        print("result testfile", result)
        
        # Prueba de excepción para búsqueda no exitosa
        with self.assertRaises(FileNotFoundError):
            print("INICIANDO findFilesByProcessUserDirectoryFilenameSizeDateTime")
            findFilesByProcessUserDirectoryFilenameSizeDateTime(
                typeProcess='LIBERATOR',
                user='CREASYSX',
                directory='salida',
                fileName='liberator-ripleyX.pdf',
                size='31859',
                date='2023-09-22',
                time='16:52:40'
            )

if __name__ == '__main__':
    print("INICIANDO TEST ----MAIN ----")
    unittest.main()