"""Main module with the code to run the Twitch bot"""

import asyncio
import logging
import os

import asqlite
import i18n
import twitchio

import efttroll
import utils
from services import RoastService
from dotenv import load_dotenv
from efttroll.bot import Bot, BotConfig
from efttroll.models import KOUCH

LOGGER: logging.Logger = logging.getLogger("Main")

if __name__ == "__main__":
    load_dotenv()
    i18n.load_path.append(os.getenv("I18N_PATH", default="../i18n/"))

    KOUCH.load_profile()

    chatgpt_service = RoastService(utils.get_mandatory_env("OPENAI_API_KEY"))

    twitchio.utils.setup_logging(level=logging.INFO)

    async def runner() -> None:
        """Run the bot"""
        async with asqlite.create_pool("tokens.db") as tdb, Bot(
            config=BotConfig.from_env(),
            chatgpt_service=chatgpt_service,
            token_database=tdb,
        ) as bot:
            await bot.setup_database()
            await bot.start()

    try:
        LOGGER.info("Running efttroll version: %s", efttroll.__version__)
        asyncio.run(runner())
    except KeyboardInterrupt:
        LOGGER.warning("Shutting down due to KeyboardInterrupt...")
