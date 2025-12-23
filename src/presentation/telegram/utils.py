import aiofiles


async def read_profanity() -> set[str]:
    async with aiofiles.open("profanity.txt", "r", encoding="utf-8") as f:
        content = await f.read()
    return set(content.lower().splitlines())
