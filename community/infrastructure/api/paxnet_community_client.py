import aiohttp
from typing import Optional


class PaxnetCommunityClient:
    BASE_URL = "https://www.paxnet.co.kr"

    def __init__(self):
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=20)
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                              "AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
            }
            self._session = aiohttp.ClientSession(timeout=timeout, headers=headers)
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def fetch_board_html(self, board_id: str, page: int = 1) -> str:
        """
        목록 HTML
        예: /tbbs/list?id=N00801&tbbsType=L&pageNo=1
        """
        params = {
            "id": board_id,
            "tbbsType": "L",
            "pageNo": str(page),   
        }
        url = f"{self.BASE_URL}/tbbs/list"

        session = await self._get_session()
        async with session.get(url, params=params, allow_redirects=True) as resp:
            resp.raise_for_status()
            return await resp.text()

    async def fetch_post_html(self, board_id: str, seq: str) -> str:
        """
        상세 HTML
        예: /tbbs/view?id=N00801&seq=953466
        """
        params = {
            "id": board_id,
            "seq": str(seq),
        }
        url = f"{self.BASE_URL}/tbbs/view"

        session = await self._get_session()
        async with session.get(url, params=params, allow_redirects=True) as resp:
            resp.raise_for_status()
            return await resp.text()
