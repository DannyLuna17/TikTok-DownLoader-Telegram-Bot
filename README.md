TikTok-DownLoader-Telegram-Bot
=======
[![CodeFactor](https://www.codefactor.io/repository/github/lunapy17/tiktok-downloader-telegram-bot/badge)](https://www.codefactor.io/repository/github/lunapy17/tiktok-downloader-telegram-bot)

Este repositorio contiene el código fuente de un bot de Telegram que permite descargar videos y audios de TikTok sin marca de agua. El bot está programado en Python y utiliza la librería python-telegram-bot para interactuar con la API de Telegram.

# Cómo funciona

El bot responde a dos comandos: /mp4 y /mp3. El usuario debe enviar un mensaje con el formato <comando> <enlace> para indicar el tipo de archivo que desea descargar y la URL del video o audio de TikTok que desea obtener. El bot entonces utiliza la API de downloader.bot para obtener la información del video o audio y descargarlo en el formato indicado.

El bot también proporciona información adicional sobre el archivo descargado, como el nombre de usuario de TikTok, la fecha de subida, la descripción y la duración junto al tamaño del archivo.

# Requisitos

* Python 3.x
* "python-telegram-bot" y "mutagen" son las únicas librerías necesarias que deben ser instaladas. Esto puede hacerse mediante el siguiente comando:
```
pip install -r requirements.txt
```

# Uso

1. Clona o descarga el repositorio a tu máquina local.
2. Obtén el [Token](https://core.telegram.org/bots/features#botfather) de tu bot de Telegram y reemplaza YOUR_BOT_TOKEN con el token de tu bot en el archivo main.py.
3. Ejecuta el archivo main.py en tu máquina local.
4. Abre el chat con tu bot de Telegram y envía el comando /mp3 {enlace} o /mp4 {enlace} seguido del enlace del video o audio de TikTok que deseas descargar. Por ejemplo:

```
/mp4 https://vm.tiktok.com/ZMYCQ9gda
```

El bot responderá con el archivo solicitado junto a información relevante del video en cuestión.

# Configuración

Antes de utilizar el bot, es necesario configurar la variable "BOT_TOKEN" con el token del bot de Telegram que se desea utilizar. Además, se puede ajustar el valor de "LIMIT_CONCURRENT_REQUESTS" para limitar el número de solicitudes simultáneas que se pueden procesar, por defecto se encuentra en 10.

# Atribuciones

Este bot de Telegram utiliza el servicio web [downloader.bot](https://downloader.bot/) para descargar videos y audios de TikTok sin marca de agua. Los derechos de autor del servicio web y de TikTok pertenecen a sus respectivos propietarios.

# Créditos
Este proyecto fue desarrollado por [LunaPy17](https://github.com/LunaPy17) y es libre de uso.

# Contribuciones

Este proyecto está abierto a contribuciones y mejoras. Siéntete libre de hacer un fork del repositorio y enviar un pull request con tus cambios o mejoras.
