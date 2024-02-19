import unittest
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
from mongo_conect import insert, find, update, delete
from file_model import Files

# Simular la conexión a la base de datos para las pruebas
def get_test_collection():
    client = MongoClient('mongodb+srv://sti-plus-developer:1Z9kQdtrwR5ZGodB@sti-plus-cluster-01.1vjognq.mongodb.net/')
    db = client['ripley-stiplus']
    process = db['capturator']
    config = db['configuration']
    return process

class TestDatabaseFunctions(unittest.TestCase):

  def setUp(self):
    self.process = get_test_collection()
    valores_item = {
      "idProceso": "122sq1213sxasdqw",
      "fechaHoraProceso": "fechaHoraProceso",
      "tipoProceso": "Capturador",
      "casilla": "FISA/TATA Canje​",
      "tiempoEjecucionGet": 10,
      "carpeta": "entrada",
      "fileName": "pdf2.pdf",
      "type": "pdf",
      "size": "112",
      "date": "28/11/2023",
      "time": "18:22:22",
      "statusFile": "Documentos_en_cloud_storage",
      "nombreBucket": "sti-plus-bucket-01",
      "nombreCarpeta": "banco-ripley/FISA_TATA_Canje​/FISA/TATA Canje/122sq1213sxasdqw",
      "tiempoEjecucionPut": 0
    }

    self.item = Files(**valores_item)
    # self.inserted_id = None
    self.inserted_id = '65661851a4c9c7545be71db3'

  def test_insert(self):
    print("test_insert")
    print(self.item)
    self.inserted_id = insert(self.item)
    print(self.inserted_id)
    result = self.process.find_one({"_id": ObjectId(self.inserted_id)})
    print(result)
    self.assertIsNotNone(result)

  def test_find(self):
    print("test_find_1")
    print(self.item)
    print("test_find_2")
    print(self.inserted_id)
    result = find(self.inserted_id)
    print(self.inserted_id)
    self.assertIsNotNone(result)
    self.assertEqual(result['name'], self.item.name)

  def test_update(self):
    #insert(self.item)
    #self.inserted_id = str(self.item.id)
    print("test_find")
    print(self.inserted_id)
    status = 'Documentos en casilla'
    updated_item = self.item
    updated_item.status=status
    update(self.inserted_id, updated_item)
    result = self.process.find_one({"_id": ObjectId(self.inserted_id)})
    print("line 46",result)
    self.assertEqual(result['description'], status)

  def test_delete(self):
    #insert(self.item)
    #self.inserted_id = str(self.item.id)
    delete(self.inserted_id)
    result = self.process.find_one({"_id": ObjectId(self.inserted_id)})
    self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()