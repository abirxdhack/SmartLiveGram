from telethon import TelegramClient
from utils import LOGGER
from config import API_ID, API_HASH

LOGGER.info("Creating Bot Client From BOT_TOKEN")

Irene = TelegramClient(
    "SmartLiveGram",
    api_id=API_ID,
    api_hash=API_HASH
)

LOGGER.info("Bot Client Created Successfully!")
