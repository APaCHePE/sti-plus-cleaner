import os
import sys
from dotenv import load_dotenv
sys.path.append('app')
from app.service import UsersService
# from modules.logging.logging_default import logger

load_dotenv()

def main():
    print("Iniciando captura de datos... v1.0.1")
    casilla = os.getenv('CASILLA')
    config = os.getenv('CONFIG')
    print(f"casilla->{casilla}")
    print(f"config->{config}")
    UsersService.cleaner(casilla, config)
if __name__ == "__main__":
    main()
