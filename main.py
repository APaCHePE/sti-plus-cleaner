import socket
import os

try:
    host = os.environ["HOST_IP"]
except KeyError:
    host = "0.0.0.0"

try:
    port = int(os.environ["HOST_PORT"])
except KeyError:
    port = 22

print("Host Origen: {}".format(socket.gethostbyname(socket.gethostname())))

timeout_seconds = 1
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(timeout_seconds)
result = sock.connect_ex((host, int(port)))
if result == 0:
    print("Host Destino: {}, Port: {} - True".format(host, port))
else:
    print("Host Destino: {}, Port: {} - False".format(host, port))
sock.close()
