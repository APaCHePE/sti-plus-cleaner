# mysqlconect.py

import mysql.connector
import unittest

def test_mysql_connection():
    try:
        # Configura los detalles de conexión a tu base de datos MySQL
        connection = mysql.connector.connect(
            host="35.236.216.155",
            user="root",
            password="",
            database="stiplus"
        )

        # Intenta realizar una consulta de prueba
        cursor = connection.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()

        # Verifica que la conexión y la consulta fueron exitosas
        assert result[0] == 1, "Error en la prueba de conexión a MySQL: No se recibió el resultado esperado."

    except mysql.connector.Error as e:
        # Maneja cualquier error de conexión a MySQL
        raise AssertionError(f"Error en la prueba de conexión a MySQL: {e}")

    finally:
        # Cierra la conexión
        if connection.is_connected():
            cursor.close()
            connection.close()

class TestMySQLConnection(unittest.TestCase):

    def test_connection(self):
        test_mysql_connection()

if __name__ == '__main__':
    unittest.main()