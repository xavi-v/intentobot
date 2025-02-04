import telebot
import openai
import schedule
import time
import threading
from flask import Flask
import datetime
import pytz
import os

#✨ Esto lo escribí en Replit, asi bien rata 🐁
#✨ ni idea donde chucha será su deploy ✨
# 🚨  variables de entorno
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHAT_ID = os.getenv("CHAT_ID")

# Inicializar el bot de Telegram
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Configurar OpenAI
openai.api_key = OPENAI_API_KEY

# Configurar Flask para evitar que Replit se duerma
app = Flask(__name__)

@app.route('/')
def home():
    return "El bot está corriendo😘🔥"

def run_flask():
    app.run(host="0.0.0.0", port=8080)

# 📌 Definir la zona horaria de Chile
CHILE_TZ = pytz.timezone("America/Santiago")

# 📌 Función para obtener la hora de Chile
def obtener_hora_chile():
    return datetime.datetime.now(CHILE_TZ).strftime("%H:%M")

# 📌 Función para responder mensajes con GPT-4o-mini
@bot.message_handler(func=lambda message: True)
def responder_mensaje(message):
    try:
        hora_chile = obtener_hora_chile()  # 🔹 Obtener la hora real de Chile

        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"La hora actual en Chile es {hora_chile}. Responde de acuerdo a esta información."},
                {"role": "user", "content": message.text}
            ]
        )

        respuesta = response.choices[0].message.content
        bot.send_message(message.chat.id, respuesta if respuesta else "No entendí bien, nena. 😢")

    except Exception as e:
        error_mensaje = f"Error: {str(e)}"
        print(error_mensaje)  # 🔹 Imprime el error en la consola
        bot.send_message(message.chat.id, f"Hubo un error, 😢\n{error_mensaje}")

# 📌 Función para enviar mensajes automáticos con la hora de Chile
def enviar_mensaje_diario():
    try:
        hora_chile = obtener_hora_chile()  # 🔹 Obtener la hora real de Chile
        mensaje = f"Hola Javi 💕 Son las {hora_chile} en Chile. ¿Cómo va tu día y tu avance? Recuerda mantener abierto chatGPT 🤖"

        print(f"⏳ Intentando enviar mensaje programado a las {hora_chile}...")  # 🔹 Log en consola
        bot.send_message(CHAT_ID, mensaje)
        print("✅ Mensaje enviado con éxito.")  

    except Exception as e:
        print(f"❌ Error al enviar mensaje automático: {e}") 


schedule.every().day.at("13:00").do(enviar_mensaje_diario)
# 🔹 10:00 en Chile
schedule.every().day.at("14:00").do(enviar_mensaje_diario)  
schedule.every().day.at("15:00").do(enviar_mensaje_diario)  
schedule.every().day.at("18:00").do(enviar_mensaje_diario)
# 🔹 15:00 en Chile
schedule.every().day.at("19:00").do(enviar_mensaje_diario)  
schedule.every().day.at("20:00").do(enviar_mensaje_diario)  
schedule.every().day.at("23:25").do(enviar_mensaje_diario)  
schedule.every().day.at("00:00").do(enviar_mensaje_diario)
# 🔹 21:00 en Chile
schedule.every().day.at("01:15").do(enviar_mensaje_diario)
# 🔹 22:15 en Chile



def run_schedule():
    while True:
        print("⏳ Revisando mensajes programados...")  # 🔹 Log en consola
        schedule.run_pending()
        time.sleep(300)  # 🔹 Revisión cada 5 minutos para evitar exceso de uso


threading.Thread(target=run_schedule, daemon=True).start()
threading.Thread(target=run_flask, daemon=True).start()

# Iniciar el bot
print("Bot en ejecución...")
bot.polling()

