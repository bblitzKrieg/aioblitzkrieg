import asyncio
import ssl
from typing import Optional
import time

import certifi
from aiohttp import ClientSession, TCPConnector
from aiohttp.typedefs import StrOrURL
from aiohttp.client import ClientResponse

from .exceptions import BlitzkriegAPIError


class BaseClient:
    """
    Base aiohttp client

    Set defaults on object init.
        By default `self._session` is None.
        It will be created on a first API request.
        The second request will use the same `self._session`.
    """

    def __init__(self, bypass_429: bool = True) -> None:
        
        self._session: Optional[ClientSession] = None
        self._bypass_429: bool = bypass_429
        self._last_request_timestamp: float = time.time()
        self._loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

    def get_session(self, **kwargs):
        """Get cached session. One session per instance."""
        if isinstance(self._session, ClientSession) and not self._session.closed:
            return self._session

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = TCPConnector(ssl=ssl_context)

        self._session = ClientSession(connector=connector, **kwargs)
        return self._session
    
    async def _wait_till_429_is_over(self):
        """Wait till 429 is over."""

        current_time = time.time()
        time_diff = current_time - self._last_request_timestamp

        if time_diff < 0.5:
            await asyncio.sleep(0.5 - time_diff)

    async def _make_request(self, method: str, url: StrOrURL, forced_ignore_429: bool = False, **kwargs) -> dict:
        """
        Make a request.
            :param method: HTTP Method
            :param url: endpoint link
            :param kwargs: data, params, json and other...
            :return: status and result or exception
        """
        session = self.get_session()

        if self._bypass_429 and not forced_ignore_429:
            await self._wait_till_429_is_over()

        async with session.request(method, url, **kwargs) as response:
            self._last_request_timestamp = time.time()
            return await self._validate_response(response)

    @staticmethod
    async def _validate_response(response: ClientResponse) -> dict:
        """Validate response"""

        if response.status != 200:
            raise BlitzkriegAPIError(await response.text())

        return await response.json()

    async def close(self):
        """Close the session graceful."""
        if not isinstance(self._session, ClientSession):
            return

        if self._session.closed:
            return

        await self._session.close()