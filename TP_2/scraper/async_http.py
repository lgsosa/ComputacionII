import aiohttp
import asyncio

async def fetch_html(url, timeout=30):
    timeout_cfg = aiohttp.ClientTimeout(total=timeout)
    async with aiohttp.ClientSession(timeout=timeout_cfg) as session:
        start = asyncio.get_event_loop().time()
        async with session.get(url) as resp:
            resp.raise_for_status()
            text = await resp.text()
        end = asyncio.get_event_loop().time()
    return text, (end - start) * 1000
