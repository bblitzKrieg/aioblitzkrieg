from .base import BaseClient

from dataclasses import dataclass

from .models.archives import (
    Archive,
    ArchiveList,
    ArchiveReport
)
from .models.sellers import (
    Seller
)


class AioBlitzkrieg(BaseClient):

    """
    Blitzkrieg API client.
        Consists of API methods only.
        All other methods are hidden in the BaseClient.

    :param api_key: Your API key from @BlitzkriegAutobot
    """

    def __init__(self, api_key: str):

        super().__init__()

        self.base_url = 'http://localhost:8080/public/v1'
        self.api_key = api_key

        self.headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
    
    async def get_archives(self, limit: int = 10, offset: int = 0) -> ArchiveList:

        """

        Use this method to get a list of archives.

        Args:
            limit (int): Limit of archives to get. Default is 10. Max is 100.
            offset (int): Offset of archives to get. Default is 0.

        Returns:
            ArchiveList: ArchiveList object
        """

        url = f"{self.base_url}/archives"

        params = {
            'limit': limit,
            'offset': offset
        }

        response = await self._make_request(
            method='get', url=url, headers=self.headers, params=params
        )
        return ArchiveList(**response)
    
    async def report_archive(self, archive_id: int) -> ArchiveReport:

        """

        Use this method to get a report on the archive.

        Args:
            archive_id (int): Archive ID to get report.

        Returns:
            ArchiveReport: ArchiveReport object
        """

        url = f"{self.base_url}/report/{archive_id}"

        response = await self._make_request(
            method='get', url=url, headers=self.headers
        )
        return ArchiveReport(**response)
    
    async def get_me(self) -> Seller:

        """
        Use this method to test your API key. Requires no parameters. On success, returns basic information about an app.

        Returns:
            Seller: Current profile
        """

        url = f"{self.base_url}/me"

        response = await self._make_request(
            method='get', url=url, headers=self.headers
        )
        return Seller(**response)