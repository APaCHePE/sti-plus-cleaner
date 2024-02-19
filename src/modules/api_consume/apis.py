import requests
import json
import socket
import time


def CarpetaInformacionDirectorio(url, headers, params):
    url = "https://129c0e02-9890-4121-8043-80748e91be18.mock.pstmn.io/api-cliente/api/casilla/carpeta/informacion?casilla=destefpe&directorio=buzon"
    
    response = requests.post(url, headers={
        "accept": "application/json",
        "authorization": "I68NL/8xQo0qVf/UdcisYQ=="
    })
    print("RESPONSE->",response)
    print(f"types response->{type(response)}")
    data = response.json()
    print("data->",data)

    return data

def CarpetaInformacionArchivo():
    url = "https://129c0e02-9890-4121-8043-80748e91be18.mock.pstmn.io/api-cliente/api/casilla/carpeta/archivo/informacion?archivo=PAGOSRESP20231015.RES&casilla=destefpe"

    response = requests.get(url, headers={
        "accept": "application/json",
        "authorization": "I68NL/8xQo0qVf/UdcisYQ=="
    })
    data = response.json()

    return data

def CarpetaInformacionDirectorioDynamic(url, configHeaders, configParams):
    url = str(url) + "?" + configParams[0].name + "=" + configParams[0].value + "&" + configParams[1].name + "=" + configParams[1].value
    # headers = {header.name: header.value for header in configHeaders}
    # params = {param.name: param.value for param in configParams}
    header= {
        configHeaders[0].name: configHeaders[0].value,
        configHeaders[1].name: configHeaders[1].value,
    }

    try:
        response = requests.request("GET", url, headers=header, verify=False)
        # response.raise_for_status()  # Lanza una excepción si la respuesta es un código de estado no exitoso
        response_text = response.text
        # Limpiar y cargar el JSON
        json_data = clean_json(response_text)
        # data = response.json()
        return json_data

    except Exception as err:
        print(f"error: {err}")
        print(f"Error en la solicitud: {err}")
        return None
    
def clean_json(text):
    # Filtrar caracteres no imprimibles
    cleaned_text = ''.join(char for char in text if char.isprintable())

    # Intentar cargar el JSON
    try:
        json_data = json.loads(cleaned_text)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
        return None

    
def Prueba():
    try: #https://192.168.212.1/api-cliente/api/casilla/carpeta/informacion
        base_url ='https://192.168.212.1/api-cliente/api/casilla/carpeta/informacion'
        print(f"base_url: {base_url}")

        casilla = 'despat01'
        print(f"casilla: {casilla}")

        directorio = 'buzon'
        print(f"directorio: {directorio}")

        token = 'MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAL/aibxMOyE6ikPlRmegiID2J49yIlOJ9JoC/4HRrDmhjbJE2iU3LGt3Kzk6X8AG1VsV3xNzcIQoPVd+8WiOM3UCAwEAAQ=='
        print(f"token: {token}")

        # Probar url apidir?casilla=destefpe&directorio=buzon
        url = base_url + f"?casilla={casilla}&directorio={directorio}"
        print(f"url: {url}")

        headers = {
            "authorization": f"{token}",
            "accept": "application/json"
        }

        response = requests.request("GET", url, headers=headers, verify=False)

        print(response.text)
        print(response.json())
        print(response.status_code)
        print(response.headers)
    except Exception as err:
        print(f"error: {err}")
        
def Socket(ip, port):
    try:
        ipup = False
        for i in range(retry):
                if isOpen(ip, port):
                        ipup = True
                        break
                else:
                        time.sleep(delay)
        return ipup
    except Exception as err:
        print(f"error Socket: {err}")

def isOpen(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
                s.connect((ip, int(port)))
                s.shutdown(socket.SHUT_RDWR)
                return True
        except:
                return False
        finally:
                s.close()
    except Exception as err:
        print(f"error isOpen: {err}")
                
retry = 5
delay = 10
timeout = 3