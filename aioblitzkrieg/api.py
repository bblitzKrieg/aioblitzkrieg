from .base import BaseClient

from dataclasses import dataclass
import aiofiles

from .models.archives import (
    Archive,
    ArchiveMinify,
    ArchiveList,
    ArchiveReport
)
from .models.sellers import (
    Seller
)

from aiohttp import FormData


class AioBlitzkrieg(BaseClient):

    """
    Blitzkrieg API client.
        Consists of API methods only.
        All other methods are hidden in the BaseClient.

    :param api_key: Your API key from @BlitzkriegAutobot
    """

    def __init__(self, api_key: str):

        super().__init__()

        self.base_url = 'http://api.blitzkrieg.space/public/v1'
        self.upload_base_url = 'http://uploadapi.blitzkrieg.space'
        self.api_key = api_key

        self.headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
    
    async def upload_archive(self, file_path: str, ref_id: str = None) -> ArchiveMinify:

        """

        Use this method to upload an archive.

        Args:
            file_path (str): Path to the file to upload.
            ref_id (str (optional)): The unique identifier of the referral partner. If you are not a referral partner of the service, skip this argument.

        Returns:
            ArchiveMinify: ArchiveMinify object
        """

        me = await self.get_me()

        async with aiofiles.open(file_path, 'rb') as file:

            form_data = FormData()

            file_content = await file.read()
            form_data.add_field(
                'file',
                file_content,
                filename=file_path,
                content_type='application/octet-stream'
            )

            url = f"{self.upload_base_url}/archives/upload"

            params = {
                'seller_id': me.id
            }

            if ref_id:
                params['ref_id'] = ref_id
            
            response = await self._make_request(
                method='post', url=url,
                headers=self.headers, params=params,
                data=form_data, forced_ignore_429=True
            )
            return ArchiveMinify(**response)
    
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