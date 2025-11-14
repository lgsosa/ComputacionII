import asyncio
import aiohttp
import json

async def main():
    url="https://example.com"
    endpoint="http://127.0.0.1:8000/scrape"
    async with aiohttp.ClientSession() as s:
        async with s.get(endpoint,params={"url":url}) as r:
            print(json.dumps(await r.json(),indent=2))

if __name__=="__main__":
    asyncio.run(main())
