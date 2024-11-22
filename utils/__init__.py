"""Util functions"""
import os


def get_mandatory_env(env: str) -> str:
    """Get mandatory environment variable"""
    env_value = os.getenv(env)
    assert env_value is not None, f"{env} env var not set"
    return env_value