"""Services to be used by the bot"""

from openai import OpenAI


class ChatGptService:
    """ChatGpt service"""

    def __init__(self, open_api_key: str):
        self.client = OpenAI(api_key=open_api_key)

    def roast(self, name: str) -> str:
        """Roast streamer"""
        input_message: str = (
            f"""Haz un roast al streamer {name} que acaba de morir en Escape From Tarkov jugando como PMC.\n
            Se especialmente duro e intenta hacerlo en menos de 200 caracteres."""
        )
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
        print(response)
        return response.content

    def roast_cheater(self, name: str) -> str:
        """Roast a streamer because he has been killed by a cheater"""
        input_message: str = (
            f"""Haz un roast al streamer {name} que acaba de morir en Escape From Tarkov 
            jugando como PMC por culpa de un cheto.\n
            Se especialmente duro e intenta hacerlo en menos de 200 caracteres."""
        )
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

    def roast_game(self, name: str, game: str) -> str:
        """Roast a streamer because of the game he is playing"""
        input_message: str = (
            f"""Imaginate que eres un bot de twitch al que le han pedido que haga roast a streamers.
Haz un roast al streamer {name} porque esta jugando al juego {game}. 
{name} suele jugar a Escape From Tarkov y es conocido por hacer canciones con rima y de risa en youtube sobre Escape From Tarkov.
{name} se caracteriza por llevar una mascara rosa en sus streams. 
Se especialmente ingenioso, intenta hacerlo en menos de 200 caracteres."""
        )
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
