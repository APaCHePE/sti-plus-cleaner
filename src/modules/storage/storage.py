import os
from google.cloud import storage
import tempfile

def download():
    blob_name = "banco-ripley/"
    bucket_name = "sti-plus-bucket-01"
    print("Descargando archivo...", blob_name, bucket_name)
    
    ABSOLUTE_PATH = os.path.abspath(os.getenv('SERVICE_ACCOUNT'))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ABSOLUTE_PATH
    
    storage_client = storage.Client()
    try:
        # Obtén el bucket
        bucket = storage_client.get_bucket(bucket_name)
        # Lista los blobs en la carpeta especificada
        blobs = [blob for blob in bucket.list_blobs(prefix=blob_name) if blob.name != blob_name]
        # Imprime los nombres de los blobs
        print("Archivos en la carpeta", blob_name, ":")
        for blob in blobs:
            print(blob.name)

        return blobs
    except Exception as e:
        print(e)
        return False

# upload_bucket("prueba", os.path.join(file_path, "vida.docx"), "vida-devolucion")
def upload(file_in_memory, filename, casilla, bucket_name):
    try:
        blob_name =f"{casilla}"
        ABSOLUTE_PATH = os.path.abspath(os.getenv('SERVICE_ACCOUNT'))
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ABSOLUTE_PATH #os.getenv('SERVICE_ACCOUNT')
        print("Subiendo archivo...", os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
        print("filename...", filename)
        print("casilla...", casilla)
        print("bucket_name...", bucket_name)
        
        storage_client = storage.Client()

        # Obtiene el bucket
        bucket = storage_client.get_bucket(bucket_name)

        # Crea un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_in_memory)

        # Define el nombre del blob con la carpeta y el nombre del archivo
        blob_path = f"{blob_name}/{filename}"

        # Sube el archivo al bucket
        blob = bucket.blob(blob_path)
        blob.upload_from_filename(temp_file.name)
        
        print(f"Archivo {filename} subido a {blob.public_url}")
        #return [blob.public_url for blob in bucket.list_blobs(prefix=f"{blob_name}/")]
        return blob.public_url

    except Exception as e:
        print(f"Error en la carga a Cloud Storage: {e}")
        return None