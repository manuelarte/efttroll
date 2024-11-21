"""Bot configuration module"""

import logging
import sqlite3
from dataclasses import dataclass

import asqlite
import i18n
import twitchio
from twitchio.ext import commands
from twitchio import eventsub, User

from efttroll.models import KOUCH, TarkovStreamer
from efttroll.services import RoastService

LOGGER: logging.Logger = logging.getLogger("Bot")


@dataclass
class BotConfig:
    """Bot configuration class"""

    client_id: str
    client_secret: str
    bot_id: str
    owner_id: str


class Bot(commands.Bot):
    """Twitch Chat bot configuration"""

    bot_id: str
    owner_id: str

    def __init__(
        self,
        config: BotConfig,
        chatgpt_service: RoastService,
        *,
        token_database: asqlite.Pool,
    ) -> None:
        self.token_database = token_database
        self.chatgpt_service = chatgpt_service
        super().__init__(
            client_id=config.client_id,
            client_secret=config.client_secret,
            bot_id=config.bot_id,
            owner_id=config.owner_id,
            prefix="!",
        )

    async def setup_hook(self) -> None:
        """Code to be executed once the bot is running"""
        await self.add_component(MyComponent(self.chatgpt_service))

        # Subscribe to read chat (event_message) from our channel as the bot...
        # This creates and opens a websocket to Twitch EventSub...
        subscription = eventsub.ChatMessageSubscription(
            broadcaster_user_id=KOUCH.twitch_id, user_id=self.bot_id
        )
        await self.subscribe_websocket(payload=subscription)

        # Subscribe and listen to when a stream goes live...
        # For this example listen to our own stream...
        subscription = eventsub.StreamOnlineSubscription(
            broadcaster_user_id=KOUCH.twitch_id
        )
        await self.subscribe_websocket(payload=subscription)

    async def add_token(
        self, token: str, refresh: str
    ) -> twitchio.authentication.ValidateTokenPayload:
        """Add token to the database"""
        # Make sure to call super() as it will add the tokens internally and return us some data...
        resp: twitchio.authentication.ValidateTokenPayload = await super().add_token(
            token, refresh
        )

        # Store our tokens in a simple SQLite Database when they are authorized...
        query = """
        INSERT INTO tokens (user_id, token, refresh)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id)
        DO UPDATE SET
            token = excluded.token,
            refresh = excluded.refresh;
        """

        async with self.token_database.acquire() as connection:
            await connection.execute(query, (resp.user_id, token, refresh))

        LOGGER.info("Added token to the database for user: %s", resp.user_id)
        return resp

    async def load_tokens(self, path: str | None = None) -> None:
        """Load tokens from the database"""
        # We don't need to call this manually, it is called in .login() from .start() internally...

        async with self.token_database.acquire() as connection:
            rows: list[sqlite3.Row] = await connection.fetchall(
                """SELECT * from tokens"""
            )

        for row in rows:
            await self.add_token(row["token"], row["refresh"])

    async def setup_database(self) -> None:
        """Set up the database to be used to store the tokens"""
        # Create our token table, if it doesn't exist...
        query = """CREATE TABLE IF NOT EXISTS tokens(user_id TEXT PRIMARY KEY, token TEXT NOT NULL, refresh TEXT NOT NULL)"""
        async with self.token_database.acquire() as connection:
            await connection.execute(query)

    async def event_ready(self) -> None:
        """Event triggered when the bot is ready to go"""
        LOGGER.info("Successfully logged in as: %s", self.bot_id)


class MyComponent(commands.Component):
    """Command handler"""

    chatgpt_service: RoastService

    def __init__(self, chatgpt_service: RoastService) -> None:
        # Passing args is not required...
        self.chatgpt_service = chatgpt_service

    # We use a listener in our Component to display the messages received.
    @commands.Component.listener()
    async def event_message(self, payload: twitchio.ChatMessage) -> None:
        """Holder to show how to handle all the messages"""
        print(f"[{payload.broadcaster.name}] - {payload.chatter.name}: {payload.text}")

    @commands.command()
    async def paquete(self, ctx: commands.Context) -> None:
        """Command to roast the streamer because he got killed by a cheater!

        !paquete
        """
        response = self.chatgpt_service.roast_streamer(KOUCH)
        await ctx.reply(f"{response}!")

    @commands.command(aliases=["chetazo"])
    async def cheto(self, ctx: commands.Context) -> None:
        """Command to roast the streamer because he got killed by a cheater!

        !cheto, !chetazo
        """
        response = self.chatgpt_service.roast_dying_of_cheater(KOUCH)
        await ctx.reply(f"{response}!")

    @commands.command()
    async def carrito(self, ctx: commands.Context, carrier: User | None = None) -> None:
        """Command to roast the streamer because he got killed by a cheater!

        !carrito @<carrier>
        """
        # TODO, not working the User transformer, because I stll get an exception
        streamer: TarkovStreamer = KOUCH
        if carrier is None:
            help_response = i18n.t("efttroll.roast_getting_carried.help", locale=streamer.locale)
            await ctx.reply(help_response)
        else:
            response = self.chatgpt_service.roast_getting_carried(streamer, carrier.name)
            await ctx.reply(f"{response}!")

    @commands.Component.listener()
    async def event_stream_online(self, payload: twitchio.StreamOnline) -> None:
        """Event dispatched when a user goes live from the subscription we made above"""
        # Event dispatched when a user goes live from the subscription we made above...

        # Keep in mind we are assuming this is for ourselves
        # others may not want your bot randomly sending messages...
        # await payload.broadcaster.send_message(
        #    sender=self.bot.bot_id,
        #    message=f"Hi... {payload.broadcaster}! You are live!",
        # )
        pass
