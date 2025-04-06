import asyncio
from collections.abc import AsyncGenerator, Callable, Iterator
from typing import TypeVar, cast

T = TypeVar("T")


async def run_async(func: Callable[[], T]) -> T:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func)


async def generate_async(iterator: Iterator[T]) -> AsyncGenerator[T]:
    def get_next_item() -> tuple[bool, T | None]:
        try:
            return True, next(iterator)
        except StopIteration:
            return False, None

    while True:
        has_more, item = await run_async(get_next_item)
        if has_more is True:
            yield cast("T", item)
        else:
            break
