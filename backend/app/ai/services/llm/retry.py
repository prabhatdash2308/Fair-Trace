"""
Retry management with exponential backoff.
"""
import time
import logging
from typing import Callable, Any
from .exceptions import RateLimitError, ProviderError

logger = logging.getLogger(__name__)

class RetryManager:
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        
    def execute(self, func: Callable[[], Any], correlation_id: str) -> Any:
        attempts = 0
        while attempts <= self.max_retries:
            try:
                return func()
            except RateLimitError as e:
                attempts += 1
                if attempts > self.max_retries:
                    logger.error(f"[{correlation_id}] Max retries exceeded.")
                    raise
                delay = self.base_delay * (2 ** (attempts - 1))
                logger.warning(f"[{correlation_id}] Rate limited. Retrying in {delay}s...")
                time.sleep(delay)
            except ProviderError as e:
                # Decide which provider errors are retryable
                raise
