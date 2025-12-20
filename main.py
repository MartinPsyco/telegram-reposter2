import os
from telethon import TelegramClient, events

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

GROUP_ID = int(os.getenv("GROUP_ID"))
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
REPLACE_FROM = os.getenv("REPLACE_FROM")
REPLACE_TO = os.getenv("REPLACE_TO")

client = TelegramClient("anon", API_ID, API_HASH)

async def main():
    await client.start(bot_token=BOT_TOKEN)

    @client.on(events.NewMessage(chats=CHANNEL_USERNAME))
    async def handler(event):
        text_mod = event.raw_text.replace(REPLACE_FROM, REPLACE_TO)
        await client.send_message(GROUP_ID, text_mod)

    await client.run_until_disconnected()

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())