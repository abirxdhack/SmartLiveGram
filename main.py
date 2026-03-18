import asyncio
from utils import LOGGER
from app import Irene
from config import BOT_TOKEN
from modules.group import setup_group_handler
from modules.listen import setup_listen_handler
from modules.status import setup_status_handler


async def main():
    LOGGER.info("Initializing bot handlers...")
    setup_group_handler(Irene)
    setup_listen_handler(Irene)
    setup_status_handler(Irene)
    LOGGER.info("Bot handlers initialized successfully")
    await Irene.start(bot_token=BOT_TOKEN)
    LOGGER.info("Bot Successfully Started!💥")
    await Irene.run_until_disconnected()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER.info("Bot Stopped Successfully!")
    except Exception as e:
        LOGGER.error(f"Fatal error: {e}")