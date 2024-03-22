import asyncio
import logging

import httpx
from aiolimiter import AsyncLimiter

# Error codes
ERROR_CODE_CONNECTION = 1
ERROR_CODE_TIMEOUT = 2
ERROR_CODE_REQUEST_ERROR = 3

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logfile.log")],
)


def handle_exception(url, e):
    """
    Handle exceptions and log errors.

    Args:
        url (str): The URL for which the exception occured.
        e (Exception): The exception

    Returns:
        httpx.Response: A response with an appropriate error code.
    """
    error_message = (
        f"Error occurred for URL: {url}, Error: {type(e).__name__}, message {e}"
    )
    logging.error(error_message)
    if isinstance(e, httpx.RequestError):
        return httpx.Response(status_code=ERROR_CODE_REQUEST_ERROR)
    elif isinstance(e, httpx.TimeoutException):
        return httpx.Response(status_code=ERROR_CODE_TIMEOUT)
    elif isinstance(e, httpx.ConnectError):
        return httpx.Response(status_code=ERROR_CODE_CONNECTION)
    else:
        return httpx.Response(status_code=ERROR_CODE_REQUEST_ERROR)


async def async_request_data(client, url, limiter, retry_count=3):
    """
    Asynchronously request data from a URL using an HTTP client.

    Args:
        client (httpx.AsyncClient): The HTTP client to use.
        url (str): The URL to request data from.
        limiter (aiolimiter.AsyncLimiter): An async limiter for rate limiting.
        retry_count (int): The maximum number of retries failed for failed request.

    Return:
        httpx.Response: The HTTP response.
    """
    async with limiter:
        try:
            response = await client.get(
                url, follow_redirects=True, timeout=httpx.Timeout(30.0)
            )
            return response
        except (httpx.RequestError, httpx.TimeoutException, httpx.ConnectError) as e:
            return handle_exception(url, e)


async def async_request_publisher_data(client, urls, limiter):
    """
    Asynchronously request data from multiple URLs using an HTTP client.

    Args:
        client (httpx.AsyncClient): The HTTP client to use.
        urls (list): List of URLs to request data from.
        limiter (aiolimiter.AsyncLimiter): An async limiter for rate limiting.
    Returns:
        list[httpx.Response]: List of HTTP responses.
    """
    tasks = [async_request_data(client, url, limiter) for url in urls]
    responses = await asyncio.gather(*tasks)
    return responses


def sync_request_data(client, url, retry_count=3):
    """
    Synchronously request data from a URL using an HTTP client.

    Args:
        client (httpx.Client): The HTTP client to use.
        url (str): The URL to request data from.
        retry_count (int): The maximum number of retries for failed requests.

    Returns:
        httpx.Response: The HTTP response.
    """
    try:
        response = client.get(url, follow_redirects=True, timeout=30.0)
        return response
    except (httpx.RequestError, httpx.TimeoutException, httpx.ConnectError) as e:
        return handle_exception(url, e)
