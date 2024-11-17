"""Models to be used in the app"""

import typing

import requests

from efttroll import tarkov_dev_api_url

aid_kouch: int = 5873033
twitch_id_kouch: str = "82547395"


class TarkovProfile:
    """ "Holder for the Tarkov Profile from tarkov.dev"""

    aid: int
    nickname: str

    def __init__(self, profile: dict[str, typing.Any]) -> None:
        self.aid = int(profile["aid"])
        self.nickname = profile["info"]["nickname"]


class TarkovStreamer:
    """Holder for info for the steamer"""

    twitch_id: str
    name: str
    description: str
    locale: str
    tarkov_aid: int
    # TODO, maybe store a list, so then you can compare how many times he died in the last x hours
    __tarkov_dev_profile: TarkovProfile or None

    def __init__(
        self,
        twitch_id: str,
        name: str,
        description: str,
        tarkov_aid: int,
        locale: str = "en",
    ) -> None:
        self.twitch_id = twitch_id
        self.name = name
        self.description = description
        self.locale = locale
        self.tarkov_aid = tarkov_aid

    def load_profile(self):
        """Load tarkov profile from tarkov.dev"""
        response = requests.get(tarkov_dev_api_url(self.tarkov_aid))
        if response.status_code == 200:
            self.__tarkov_dev_profile = TarkovProfile(response.json())
        else:
            raise Exception(f"Could not load profile: Response({response.status_code})")


KOUCH_DESCRIPTION = """Kouch es un streamer conocido por jugar principalmente a juegos de disparos en primera persona.
                    Su juego principal es Escape From Tarkov y su estilo de juego, se basa, principalmente en ratear.
                    Sus streams se caracterizan porque lleva un balaclava rosa y por sus alertas, que son muy divertidas."""
KOUCH: TarkovStreamer = TarkovStreamer(
    twitch_id=twitch_id_kouch,
    name="Kouch",
    description=KOUCH_DESCRIPTION,
    locale="es",
    tarkov_aid=aid_kouch,
)
