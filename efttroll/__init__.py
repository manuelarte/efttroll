"""Global project variables"""

__app_name__ = "efttroll"
__version__ = "0.0.1"


def tarkov_dev_api_url(aid: int) -> str:
    """Get the player profile from tarkov.dev"""
    return f"https://players.tarkov.dev/profile/{aid}.json"
