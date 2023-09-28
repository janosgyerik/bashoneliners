import dataclasses
import logging
from datetime import datetime
import time
from typing import Callable, Any

logger = logging.getLogger(__name__)


@dataclasses.dataclass(frozen=True)
class RateLimiterSpec:
    per_minute: int = 0
    per_day: int = 0


def compute_cool_off_seconds(spec: RateLimiterSpec):
    seconds = 0

    if spec.per_minute > 0:
        seconds = max(seconds, 1 + 60 // spec.per_minute)

    # TODO this is just too slow
    # See also: https://platform.openai.com/docs/guides/rate-limits/overview
    # Especially the part about "Example #2: Using the backoff library"
    # if spec.per_day > 0:
    #     seconds = max(seconds, 1 + 60 * 60 * 24 // spec.per_day)

    return seconds


class RateLimitedExecutor:
    def __init__(
            self,
            spec: RateLimiterSpec,
            fn: Callable[..., Any],
            timestamp_fn: Callable[[], int] = None,
            sleep_fn: Callable[[int], None] = None,
    ):
        self._fn = fn
        self._last_execution_timestamp = None
        self._cool_off_seconds = compute_cool_off_seconds(spec)

        if timestamp_fn is None:
            self._timestamp_fn = lambda: int(datetime.now().timestamp())
        else:
            self._timestamp_fn = timestamp_fn

        if sleep_fn is None:
            self._sleep_fn = lambda seconds: time.sleep(seconds)
        else:
            self._sleep_fn = sleep_fn

    def execute(self, *args, **kwargs) -> Any:
        if self._last_execution_timestamp is None:
            self._last_execution_timestamp = self._timestamp_fn()
            return self._fn(*args, **kwargs)

        elapsed_seconds = self._timestamp_fn() - self._last_execution_timestamp
        if elapsed_seconds < self._cool_off_seconds:
            to_wait_seconds = self._cool_off_seconds - elapsed_seconds
            logger.info(f"Last API call {elapsed_seconds} seconds ago. "
                        f"Waiting for {to_wait_seconds} seconds to respect rate limits...")
            self._sleep_fn(to_wait_seconds)

        self._last_execution_timestamp = self._timestamp_fn()
        return self._fn(*args, **kwargs)
