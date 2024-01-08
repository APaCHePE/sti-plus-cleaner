import unittest
from unittest.mock import patch, MagicMock
from apis import CarpetaInformacionDirectorioDynamic, CarpetaInformacionArchivo

class TestApis(unittest.TestCase):

    @patch('apis.requests.get')
    def test_carpeta_informacion_directorio(self, mock_get):
        # Configurar el objeto mock para simular la respuesta HTTP
        print("test_carpeta_informacion_directorio")
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "value"}
        mock_get.return_value = mock_response

        # Llamar a la función que estás probando
        result = CarpetaInformacionDirectorioDynamic()
        print(result)
        # Verificar que se llamó a la función requests.get con la URL y encabezados correctos
        """mock_get.assert_called_once_with(
            "https://129c0e02-9890-4121-8043-80748e91be18.mock.pstmn.io/api-cliente/api/casilla/carpeta/informacion?casilla=destefpe&directorio=buzon",
            headers={
                "accept": "application/json",
                "authorization": "I68NL/8xQo0qVf/UdcisYQ=="
            }
        )"""

        # Verificar que la función devuelve el resultado esperado
        # self.assertEqual(result, {"key": "value"})

    @patch('apis.requests.get')
    def test_carpeta_informacion_archivo(self, mock_get):
        # Configurar el objeto mock para simular la respuesta HTTP
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "value"}
        mock_get.return_value = mock_response

        # Llamar a la función que estás probando
        result = CarpetaInformacionArchivo()

        # Verificar que se llamó a la función requests.get con la URL y encabezados correctos
        mock_get.assert_called_once_with(
            "https://192.168.212.1/api-cliente/api/casilla/carpeta/archivo/informacion?archivo=PAGOSRESP20231015.RES&casilla=destefpe",
            headers={
                "accept": "application/json",
                "authorization": "I68NL/8xQo0qVf/UdcisYQ=="
            }
        )

        # Verificar que la función devuelve el resultado esperado
        self.assertEqual(result, {"key": "value"})

if __name__ == '__main__':
    unittest.main()