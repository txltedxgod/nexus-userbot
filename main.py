import sys
import os
import asyncio
import signal
from pathlib import Path

from nexus.config import config
from nexus.client import NexusClient
from nexus.logger import get_logger

logger = get_logger("launcher")

BANNER = r"""
  _   _ _______   ___   _ _____ 
 | \ | | ____\ \ / / | | / ___|
 |  \| |  _|  \ V /| | | \___ \ 
 | |\  | |___  | | | |_| |___) |
 |_| \_|_____| |_|  \___/|____/ 
   ✦ NEXT-GEN TELEGRAM USERBOT ✦
"""

async def run_userbot():
    print("\033[96m" + BANNER + "\033[0m")
    logger.info("Initializing Nexus Userbot runtime...")

    if not config.API_ID or not config.API_HASH:
        logger.critical("API_ID or API_HASH not found in environment (.env).")
        logger.info("Please copy .env.example to .env and provide your Telegram API credentials.")
        return

    client = NexusClient()
    authorized = await client.initialize()
    if not authorized:
        logger.error("Authorization required. Start client interactively to sign in.")
        return

    logger.info("✦ Nexus Userbot is actively running in background! Press Ctrl+C to terminate.")

    # Loop until disconnected
    await client.run_until_disconnected()

def main():
    try:
        asyncio.run(run_userbot())
    except KeyboardInterrupt:
        logger.info("Nexus Userbot terminated by user. Goodbye!")
    except Exception as e:
        logger.critical(f"Fatal error in userbot lifecycle: {e}", exc_info=True)

if __name__ == "__main__":
    main()
