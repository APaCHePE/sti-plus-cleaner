import os
import sys
from dotenv import load_dotenv
sys.path.append('app')
from app.service import UsersService
# from modules.logging.logging_default import logger

load_dotenv()

def main():
    print("Iniciando captura de datos... v1.0.1")
    
    user = os.getenv('USER')
    process = os.getenv('PROCESS')
    print(f"USER->{user}|PROCESS->{process}")
    UsersService.cleaner(user, process)
if __name__ == "__main__":
    main()
