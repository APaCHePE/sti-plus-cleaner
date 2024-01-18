# Título del Proyecto

Breve descripción del proyecto y su propósito.

## Tabla de Contenidos

- [Instalación](#instalación)
- [Uso](#uso)
- [Ejemplos](#ejemplos)
- [Configuración](#configuración)
- [Contribución](#contribución)
- [Licencia](#licencia)

## Instalación

Indica cómo instalar y configurar el proyecto. Proporciona comandos y requisitos específicos, si los hay.

```bash
# Crear entorno virtual
python -m venv env 
# Activar entorno virtual
env\Scripts\activate 
# En mi caso actualizar PIP
python.exe -m pip install --upgrade pip
# instalar Requeriments
pip install -r requirements.txt
# Levantar el proyecto
uvicorn main:apps  --reload --host 0.0.0.0 --port 8000
# excecute test unit
pytest -k "test_insert" test_mongo.py
pytest -k "test_carpeta_informacion_directorio" modules/api_consume/apis_test.py

uvicorn src.main:app --reload --port=8000 --host=0.0.0.0  
python> docker compose up --build  

uvicorn main:apps --reload --port=8000 --host=0.0.0.0  
uvicorn src.main:app --reload --port=8080 --host=0.0.0.0    
python -m uvicorn main:app --reload  
pip freeze > requeriments.txt      
desactivate
```
> docker compose -f docker-cpose.development.yaml up --build   
e
***
## Python

Validar versiones de PIP
*pip --version*
## Instalar 
*pip install flask*
*pip install os*
*pip install --user uvicorn*

## PYTHON RUN
*python app.py*
## COMPOSE UP DOCKER 
docker compose up
## COMPOSE DEV DOCKER 
*docker compose -f docker-compose.development.yaml up*
## COMPOSE PROD DOCKER 
*docker compose -f docker-compose.production.yaml up --build -d*
## BUILD DOCKER 
*docker build -t apradoch/sti-cleaner:1.0.0 .*
## PUSH DOCKER 
*docker push apradoch/sti-cleaner:1.0.0*

## docker recuperar imagen docker
*docker pull apradoch/sti-cleaner:1.0.0* 
## retageo a formato GCP
*docker tag apradoch/sti-cleaner:1.0.1 us-east4-docker.pkg.dev/br-gcp-sti-pp/repos-docker/sti-cleaner:v1.0.0*
## push imagen a Artifactory Registry
*docker push us-east4-docker.pkg.dev/br-gcp-sti-pp/repos-docker/sti-cleaner:v1.0.0*