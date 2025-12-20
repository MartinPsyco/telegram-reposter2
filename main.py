import os
from telethon import TelegramClient, events

# Variables de entorno (Railway las inyecta automáticamente)
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

GROUP_ID = int(os.getenv("GROUP_ID"))
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
REPLACE_FROM = os.getenv("REPLACE_FROM")
REPLACE_TO = os.getenv("REPLACE_TO")
# Debug opcional: imprime credenciales para verificar que Railway las pasa bien
print("API_ID:", API_ID)
print("API_HASH:", API_HASH)
print("BOT_TOKEN:", BOT_TOKEN[:10], "...")

# Inicializa el cliente directamente con el bot token

client = TelegramClient("reposter_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)
# Handler: escucha mensajes en el canal y los reenvía al grupo
@client.on(events.NewMessage(chats=CHANNEL_USERNAME))
async def handler(event):
    text_mod = event.raw_text.replace(REPLACE_FROM, REPLACE_TO)
    await client.send_message(GROUP_ID, text_mod)

print("✅ Telegram Reposter online 🚀")

# Mantiene el bot corriendo
client.run_until_disconnected()


