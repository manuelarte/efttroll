import asyncio
import logging
import os

import asqlite
import twitchio

from eft_troll.bot import Bot
from eft_troll.models import kouch
from services import ChatGptService
from dotenv import load_dotenv

LOGGER: logging.Logger = logging.getLogger("__main__")

CLIENT_ID = "0tm1ztzhhi8wzxudv57rfgawna9fz2"
CLIENT_SECRET = "e73j0ubiomqf1gejg8xxdvdixo1aep"


async def oauth() -> None:
    channel_bot = twitchio.Scopes.all()

    oauth_service = twitchio.authentication.OAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri="http://localhost:4343/oauth/callback",
        scopes=channel_bot,  # Use updated kwargs
    )

    auth_url = oauth_service.get_authorization_url(force_verify=True)
    print(auth_url)


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
        await oauth()
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
