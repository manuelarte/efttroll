import requests

from eft_troll import tarkov_dev_api_url

aid_kouch: int = 5873033


class TarkovProfile:
    """ "Holder for the Tarkov Profile from tarkov.dev"""

    aid: int

    def __init__(self, aid: int) -> None:
        self.aid = aid


class TarkovStreamer:
    aid: int
    name: str
    # TODO, maybe store a list, so then you can compare how many times he died in the last x hours
    tarkov_dev_profile: dict[str, object] or None

    def __init__(self, aid: int, name: str) -> None:
        self.aid = aid
        self.name = name

    def load_profile(self):
        profile = requests.get(tarkov_dev_api_url(self.aid))
        if profile.status_code == 200:
            print(profile.json())
            self.tarkov_dev_profile = profile.json()


kouch: TarkovStreamer = TarkovStreamer(aid=aid_kouch, name="Kouch")
