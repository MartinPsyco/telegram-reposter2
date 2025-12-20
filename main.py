import os
import re
import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

# Variables de entorno
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

# Lista de canales separados por coma
CHANNELS = os.getenv("CHANNELS", "").split(",")

REPLACE_FROM = os.getenv("REPLACE_FROM") or "@athono"
REPLACE_TO = os.getenv("REPLACE_TO") or "@Nintendo_Logs"

PRICE_PATTERN = re.compile(r'(\d+(?:\.\d+)?)\s*\$')

def adjust_text(text: str) -> str:
    if not text:
        return None
    text = text.replace(REPLACE_FROM, REPLACE_TO)
    def add_two(match):
        value = float(match.group(1))
        if value.is_integer():
            return f"{int(value + 2)}$"
        else:
            return f"{value + 2:.2f}$"
    return PRICE_PATTERN.sub(add_two, text)

# Cliente de usuario (lee canales públicos con user.session)
user_client = TelegramClient("user", API_ID, API_HASH)

# Cliente de bot (publica en grupo)
bot_client = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Filtro anti-duplicados
last_id = None

@user_client.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    global last_id

    # Evita duplicados
    if event.id == last_id:
        return
    last_id = event.id

    # Ignora mensajes viejos (más de 1 minuto)
    if event.message.date < (datetime.utcnow() - timedelta(minutes=1)):
        return

    text_mod = adjust_text(event.raw_text)

    # Pequeño delay para evitar floods
    await asyncio.sleep(0.5)

    # Si es foto o documento (incluye videos)
    if isinstance(event.message.media, (MessageMediaPhoto, MessageMediaDocument)):
        await bot_client.send_file(GROUP_ID, event.message.media, caption=text_mod)
    else:
        # Texto puro o enlaces con preview
        if text_mod:
            await bot_client.send_message(GROUP_ID, text_mod)

    print(f"✅ Mensaje {event.id} procesado y enviado")

print("✅ User+Bot Reposter online ahora funcionando bien 🚀")

user_client.start()
user_client.run_until_disconnected()
