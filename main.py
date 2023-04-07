# Importamos Librerias Necesarias
from telegram.ext import Updater, PrefixHandler
from requests import get, post
from datetime import datetime
import threading
import telegram
from telegram import ParseMode
import mutagen
from io import BytesIO

# Definimos las variables globales
BOT_TOKEN = "YOUR_BOT_TOKEN"
LIMIT_CONCURRENT_REQUESTS = 10  # Límite de solicitudes simultáneas

# Función para descargar videos o audios de TikTok sin marca de agua
def ttDL(link: str, format: str, semaphore: threading.Semaphore) -> any:
    # Definimos las cabeceras de la solicitud
    headers = {
        "authority": "downloader.bot",
        "method": "POST",
        "path": "/api/tiktok/info",
        "accept": "application/json, text/plain, */*",
        "accept-language": "es;q=0.9",
        "content-type": "application/json",
        "cookie": "",
        "origin": "https://downloader.bot",
        "referer": "https://downloader.bot/de",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }

    # Solicitamos la información del video o audio
    with semaphore:
        vid = post("https://downloader.bot/api/tiktok/info", data='''{"url":"'''+link+'''"}''', headers = headers)
        
        # Verificamos que la URL sea válida
        try:
            if vid.json()["error"] != "":
                return "INVALID URL"
        except: return "INVALID URL"
        
        # Obtenemos la información del video o audio
        mp4link = vid.json()["data"]["mp4"]
        mp3link = vid.json()["data"]["mp3"]
        vidUser = vid.json()["data"]["nick"]
        vidDate = datetime.fromtimestamp(vid.json()["data"]["video_date"]).date()
        vidDescription = vid.json()["data"]["video_info"]
        
        # Descargamos el archivo solicitado en el formato indicado
        if format == "mp4":
            return [get(mp4link).content, vidUser, vidDate, vidDescription]
        elif format == "mp3":
            return [get(mp3link).content, vidUser, vidDate, vidDescription]
        else:
            return "INVALID FORMAT"

# Función del comando para enviar el archivo
def download(update: telegram.Update, context: telegram.ext.CallbackContext) -> None:
    message = update.message
    text = message.text
    
    # Verificamos que el mensaje tenga la estructura correcta
    if text.startswith(("/mp3", "/mp4 ")):
        try: link = text.split(" ")[1]
        except: return message.reply_text("You must enter a link.")
        try:
            if not "tiktok.com" in get(link, allow_redirects=True).text: return message.reply_text("You must enter a TikTok Valid link.")
        except: return message.reply_text("You must enter a TikTok Valid link.")
        format = text.split(" ")[0][1:]
        
        # Creamos un semáforo para controlar el número máximo de solicitudes simultáneas
        semaphore = threading.Semaphore(LIMIT_CONCURRENT_REQUESTS)
        
        # Descargamos el archivo de forma síncrona
        datosVid = ttDL(link, format, semaphore)
        if datosVid == "INVALID URL": return message.reply_text("You must enter a TikTok Valid link.")
        file = datosVid[0]
        
        # obtiene la duración del archivo en segundos
        duration = (mutagen.File(BytesIO(file)).info.length)
        # convierte la duración en minutos y segundos
        minutes, seconds = divmod(duration, 60)

        # Enviamos el archivo al usuario
        if file == "INVALID URL" or file == "INVALID FORMAT":
            message.reply_text(file)
        else:
            if format == "mp4":
                message.reply_video(
                    video=file,
                    filename=f"@{datosVid[1]}-@TikTokDownLoaderMp4Bot",
                    caption=f"<b>✅ TikTok Video Downloaded Successfully</b>\n\n<b>URL</b> >>> <code>{link}</code>\n<b>User</b> >>> <code>@{datosVid[1]}</code>\n<b>Description</b> >>> <code>{datosVid[3]}</code>\n<b>Upload date</b> >>> <code>{datosVid[2]}</code>\n<b>File Size</b> >>> <code>{round(len(datosVid[0])/(1024 * 1024), 2)} MB</code>\n<b>Duration</b> >>> <code>{int(minutes)}:{int(seconds):02d}</code>",
                    parse_mode=ParseMode.HTML
                )
            elif format == "mp3":
                message.reply_audio(
                    audio=file,
                    filename=f"@{datosVid[1]}-@TikTokDownLoaderMp4Bot",
                    caption=f"<b>✅ TikTok Music Downloaded Successfully</b>\n\n<b>URL</b> >>> <code>{link}</code>\n<b>User</b> >>> <code>@{datosVid[1]}</code>\n<b>Description</b> >>> <code>{datosVid[3]}</code>\n<b>Upload date</b> >>> <code>{datosVid[2]}</code>\n<b>File Size</b> >>> <code>{round(len(datosVid[0])/(1024 * 1024), 2)} MB</code>\n<b>Duration</b> >>> <code>{int(minutes)}:{int(seconds):02d}</code>",
                    parse_mode=ParseMode.HTML
                )

# Función para el comando de bienvenida
def start(update, context): 
    message = update.message
    
    response = (
        "<b>Welcome to TikTok Downloader Bot!</b>\n\n"
        "You can download TikTok videos and music without watermark by using the commands <code>/mp4 [video_url]</code> and "
        "<code>/mp3 [video_url]</code> respectively.\n\n"
        "For example:\n"
        "<code>/mp4 https://www.tiktok.com/@bellapoarch/video/1234567890123456789</code>\n"
        "<code>/mp3 https://www.tiktok.com/@bellapoarch/video/1234567890123456789</code>\n\n"
        "If you have any questions or issues, please contact @DannyLuna.\n\n"
        "Thank you for using TikTok Downloader Bot! 🎉🎊"
    )
    
    message.reply_text(response, parse_mode=ParseMode.HTML)

if __name__ == '__main__':
    # Configramos el bot
    myBot = telegram.Bot(token=BOT_TOKEN)
    updater = Updater(token=myBot.token, use_context=True)
    dp = updater.dispatcher

    # # Agregamos los manejadores de comandos
    dp.add_handler(PrefixHandler(['!', '$', '!', '/', '.' , ',' , '-' , '>'], "mp4", download, run_async=True))
    dp.add_handler(PrefixHandler(['!', '$', '!', '/', '.' , ',' , '-' , '>'], "mp3", download, run_async=True))
    dp.add_handler(PrefixHandler(['!', '$', '!', '/', '.' , ',' , '-' , '>'], "start", start, run_async=True))

    # Iniciamos el bot
    updater.start_polling()
    updater.idle()
