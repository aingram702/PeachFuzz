import asyncio
import time
from typing import Callable, Any

async def measure_time(func: Callable, *args, **kwargs) -> Any:
    """Async wrapper to measure execution time of a function."""
    start_time = time.time()
    result = await func(*args, **kwargs)
    end_time = time.time()
    return result, end_time - start_time

def format_size(size_headers: str) -> int:
    """Safely converts content-length header to int."""
    try:
        return int(size_headers)
    except (ValueError, TypeError):
        return 0
