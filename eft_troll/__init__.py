__app_name__ = "eft_troll"
__version__ = "0.0.1"


def tarkov_dev_api_url(aid: int) -> str:
    return f"https://players.tarkov.dev/profile/{aid}.json"
