import httpx
import asyncio
from aiolimiter import AsyncLimiter

async def request_data(client, url, limiter, retry_count=3):
    async with limiter:
        try:
            response = await client.get(url, follow_redirects=True)
            return response
        except (httpx.RequestError) as e:
            print(f"Error occurred for URL: {url}, Error: {type(e).__name__}, message {e}")
            return httpx.Response(status_code=9999)

async def request_publisher_data(client, publisher, urls, limiter):
    print(f"Fetching data for publisher: {publisher}")
    tasks = [request_data(client, url, limiter) for url in urls]
    responses = await asyncio.gather(*tasks)
    return responses
