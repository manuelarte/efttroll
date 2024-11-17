"""Main module with the code to run the Twitch bot"""

import asyncio
import logging
import os

import asqlite
import twitchio

from services import ChatGptService
from dotenv import load_dotenv
from eft_troll.bot import Bot
from eft_troll.models import kouch


LOGGER: logging.Logger = logging.getLogger("__main__")


def get_mandatory_env(env: str) -> str:
    env_value = os.getenv(env)
    assert env_value is not None, f"{env} env var not set"
    return env_value


if __name__ == "__main__":
    load_dotenv()

    # kouch.load_profile()

    open_api_key = get_mandatory_env("OPENAI_API_KEY")
    chatgpt_service = ChatGptService(open_api_key)
    # output = service.roast("Kouch")

    twitchio.utils.setup_logging(level=logging.INFO)

    async def runner() -> None:
        """Run the bot"""
        async with asqlite.create_pool("tokens.db") as tdb, Bot(
            client_id=get_mandatory_env("CLIENT_ID"),
            client_secret=get_mandatory_env("CLIENT_SECRET"),
            bot_id=get_mandatory_env("BOT_ID"),
            owner_id=get_mandatory_env("OWNER_ID"),
            chatgpt_service=chatgpt_service,
            token_database=tdb,
        ) as bot:
            await bot.setup_database()
            await bot.start()

    try:
        asyncio.run(runner())
    except KeyboardInterrupt:
        LOGGER.warning("Shutting down due to KeyboardInterrupt...")
