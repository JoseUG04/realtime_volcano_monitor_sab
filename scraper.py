import time
import schedule
import requests
from datetime import datetime
import os

# URL base de las cámaras que deseas capturar
CAMARAS = {
    1: "https://ide.igp.gob.pe/ltImages/Sabancaya.jpg",       # Cámara 1
    3: "https://ide.igp.gob.pe/ltImages/Sabancaya05.jpg",     # Cámara 3
    4: "https://ide.igp.gob.pe/ltImages/Sabancaya03.jpg"      # Cámara 4
}

# Carpeta base donde se almacenarán las imágenes
CARPETA_BASE = "imagenes_sabancaya"
os.makedirs(CARPETA_BASE, exist_ok=True)

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

            with open(ruta_img, "wb") as f:
                f.write(img_data)
            print(f"[OK] Imagen de Cámara {camara_id} guardada: {ruta_img}")
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
