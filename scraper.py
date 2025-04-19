import time
import schedule
import requests
from datetime import datetime
import os
import boto3
from botocore.exceptions import NoCredentialsError

# URL base de las cámaras que deseas capturar
CAMARAS = {
    1: "https://ide.igp.gob.pe/ltImages/Sabancaya.jpg",       # Cámara 1
    3: "https://ide.igp.gob.pe/ltImages/Sabancaya05.jpg",     # Cámara 3
    4: "https://ide.igp.gob.pe/ltImages/Sabancaya03.jpg"      # Cámara 4
}

# Carpeta base donde se almacenarán las imágenes localmente
CARPETA_BASE = "imagenes_sabancaya"
os.makedirs(CARPETA_BASE, exist_ok=True)

# Configuración de Cloudflare R2
R2_BUCKET_NAME = "sabancaya-images"
R2_ACCESS_KEY = "Nb0F_Iq6HR5XtNDWCWZuVOVINriXwGGPc9X4fYFn"
R2_SECRET_KEY = "Nb0F_Iq6HR5XtNDWCWZuVOVINriXwGGPc9X4fYFn"
R2_ENDPOINT = "https://c54305f178e277d958a60034d8e72953.r2.cloudflarestorage.com"

# Crear una sesión de boto3 para interactuar con Cloudflare R2
s3_client = boto3.client(
    's3',
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY
)

# Función para cargar la imagen a Cloudflare R2
def cargar_a_r2(ruta_imagen, nombre_imagen):
    try:
        with open(ruta_imagen, 'rb') as f:
            s3_client.put_object(
                Bucket=R2_BUCKET_NAME,
                Key=nombre_imagen,
                Body=f,
                ContentType='image/jpeg'
            )
        print(f"[OK] Imagen cargada a R2: {nombre_imagen}")
    except NoCredentialsError:
        print("[ERROR] Las credenciales de R2 no son válidas o no se han proporcionado correctamente.")
    except Exception as e:
        print(f"[ERROR] No se pudo cargar la imagen a R2: {e}")

# Función para descargar imágenes de las cámaras seleccionadas
def descargar_imagenes():
    ahora = datetime.now()
    carpeta_fecha = os.path.join(CARPETA_BASE, ahora.strftime("%Y-%m-%d"))
    os.makedirs(carpeta_fecha, exist_ok=True)

    for camara_id, camara_url in CAMARAS.items():
        try:
            img_data = requests.get(camara_url).content
            nombre_img = f"{ahora.strftime('%H-%M')}_cam{camara_id}.jpg"
            ruta_img = os.path.join(carpeta_fecha, nombre_img)

            # Guardar la imagen localmente
            with open(ruta_img, "wb") as f:
                f.write(img_data)
            print(f"[OK] Imagen de Cámara {camara_id} guardada: {ruta_img}")

            # Subir la imagen a Cloudflare R2
            cargar_a_r2(ruta_img, nombre_img)
        except Exception as e:
            print(f"[ERROR] No se pudo descargar la imagen de la Cámara {camara_id}: {e}")

# Programar capturas cada 5 minutos de 07:00 a 17:55
for hora in range(7, 18):  # De 7:00 a 17:59
    for minuto in range(0, 60, 5):  # Cada 5 minutos
        schedule.every().day.at(f"{hora:02d}:{minuto:02d}").do(descargar_imagenes)

# Bucle que mantiene activo el script
while True:
    schedule.run_pending()
    time.sleep(1)
