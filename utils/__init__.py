import datetime
from typing import Callable, cast
from functools import wraps
import threading
import time


# define Python user-defined exceptions
class RateLimitedReached(Exception):
    """Raised when the rate limit is reached"""
    left_to_wait: int
    available_at: time

    def __init__(self, left_to_wait, message="Rate limit reached"):
        self.left_to_wait = left_to_wait
        self.available_at = datetime.datetime.now() + datetime.timedelta(seconds=left_to_wait)
        self.message = message
        super().__init__(self.message)


def rate_limited[T, ** P](max_per_minute: float) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def decorator(fn: Callable[P, T]) -> Callable[P, T]:
        lock = threading.RLock()
        min_interval = 60.0 / max_per_minute
        last_time_called = 0.0

        @wraps(fn)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            with lock:
                nonlocal last_time_called
                elapsed = time.perf_counter() - last_time_called
                left_to_wait = min_interval - elapsed
                if left_to_wait > 0:
                    raise RateLimitedReached(left_to_wait=left_to_wait)

                last_time_called = time.perf_counter()
                return fn(*args, **kwargs)

        return cast(Callable[P, T], wrapper)

    return decorator
