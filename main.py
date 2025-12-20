import os
import re
from telethon import TelegramClient, events

# Variables de entorno (Railway las inyecta automáticamente)
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

GROUP_ID = int(os.getenv("GROUP_ID"))

# Lista de canales separados por coma en la variable CHANNELS
CHANNELS = os.getenv("CHANNELS", "").split(",")

REPLACE_FROM = os.getenv("REPLACE_FROM") or "@athono"
REPLACE_TO = os.getenv("REPLACE_TO") or "@Nintendo_Logs"

# Regex para detectar precios en formato "26$", "26 $", "26.50$"
PRICE_PATTERN = re.compile(r'(\d+(?:\.\d+)?)\s*\$')

def adjust_text(text: str) -> str:
    if not text:
        return None
    # Reemplazo de mención
    text = text.replace(REPLACE_FROM, REPLACE_TO)
    # Ajuste de precio: suma 2 al número antes del símbolo $
    def add_two(match):
        value = float(match.group(1))
        if value.is_integer():
            return f"{int(value + 2)}$"
        else:
            return f"{value + 2:.2f}$"
    return PRICE_PATTERN.sub(add_two, text)

# Inicializa el cliente directamente con el bot token
client = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Handler: escucha mensajes en todos los canales listados y los publica en el grupo
@client.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    text_mod = adjust_text(event.raw_text)

    if event.message.media:
        await client.send_file(GROUP_ID, event.message.media, caption=text_mod)
    else:
        if text_mod:
            await client.send_message(GROUP_ID, text_mod)

print("✅ Telegram Reposter online 🚀")
client.run_until_disconnected()
