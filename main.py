#Copyright @ISmartCoder
#Updates Channel https://t.me/TheSmartProgrammers
from utils import LOGGER
from app import snigdha
from modules.listen import setup_listen_handler
from modules.status import setup_status_handler

try:
    LOGGER.info("Initializing bot handlers...")
    setup_listen_handler(snigdha)
    setup_status_handler(snigdha)
    LOGGER.info("Bot handlers initialized successfully")
    
    LOGGER.info("Bot Successfully Started!💥")
    snigdha.run()
except Exception as e:
    LOGGER.error(f"Failed to start bot: {e}")
finally:
    LOGGER.info("Bot Stopped Successfully!")