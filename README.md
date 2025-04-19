# realtime_volcano_monitor_sab

Este script descarga imágenes en tiempo real del volcán Sabancaya, utilizando las cámaras disponibles en el sitio web del IGP. Las imágenes se almacenan localmente para su posterior análisis.

## Requisitos

- Python 3.10 o superior
- Librerías de Python:
  - requests
  - BeautifulSoup
  - schedule

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/JoseUG04/realtime_volcano_monitor_sab.git
    ```

2. Instala las dependencias:
    ```bash
    pip install requests beautifulsoup4 schedule
    ```

## Uso

1. Asegúrate de tener Python instalado.
2. Ejecuta el script con:
    ```bash
    python scraper.py
    ```
3. Las imágenes serán descargadas automáticamente entre las 7:00 AM y las 5:00 PM cada 5 minutos. Las imágenes se almacenarán en la carpeta `imagenes_sabancaya`.

## Contribuciones

Si deseas contribuir a este proyecto, por favor abre un *Pull Request*.
