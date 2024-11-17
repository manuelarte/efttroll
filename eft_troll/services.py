"""Services to be used by the bot"""

from openai import OpenAI

from eft_troll.models import TarkovStreamer, TarkovProfile


class RoastService:
    """Roast service"""

    def __init__(self, open_api_key: str):
        self.client = OpenAI(api_key=open_api_key)

    def roast_streamer(self, streamer: TarkovStreamer) -> str:
        """Roast streamer"""
        input_message: str = (
            f"""Haz un roast al streamer {streamer.name}.
            Se creativo e intenta hacerlo en menos de 200 caracteres.
            Aquí tienes más información sobre {streamer.name}: {streamer.description}"""
        )
        # Add extra information about the streamer
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": input_message,
                }
            ],
            model="gpt-4o",
        )
        response = chat_completion.choices[0].message
        return response.content

    def roast_cheater(
        self, streamer: TarkovStreamer, cheater_profile: TarkovProfile or None = None
    ) -> str:
        """Roast a streamer because he/she has been killed by a cheater"""
        input_message: str = (
            f"""Haz un roast al streamer {streamer.name} que acaba de morir en Escape From Tarkov por culpa de un cheto.
            Se creativo e intenta hacerlo en menos de 200 caracteres."""
        )
        return self.__send_message__(input_message)

    def __send_message__(self, message: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            model="gpt-4o",
        )
        response = chat_completion.choices[0].message
        return response.content
