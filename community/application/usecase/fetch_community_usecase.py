from typing import List, Dict

from community.adapter.output.paxnet.community_api_adapter import PaxnetCommunityAdapter
from community.application.port.community_repository_port import CommunityRepositoryPort
from community.domain.value_object.community_post import CommunityPost


class FetchCommunityUsecase:
    def __init__(self, adapter: PaxnetCommunityAdapter, repository: CommunityRepositoryPort):
        self.adapter = adapter
        self.repository = repository

    async def fetch_latest(self, board_id: str, page: int, limit: int = 50) -> List[CommunityPost]:
        return await self.adapter.fetch_latest(board_id=board_id, page=page, max_posts=limit)

    async def fetch_latest_from_db(self, board_id: str, page: int = 1, limit: int = 20) -> List[CommunityPost]:
        return await self.repository.find_latest_posts(board_id=board_id, page=page, limit=limit)

    async def fetch_and_save_latest(self, board_id: str, page: int, limit: int = 100) -> Dict:
        posts = await self.adapter.fetch_latest(board_id=board_id, page=page, max_posts=limit)
        if not posts:
            return {"saved_count": 0, "items": []}

        saved_count = await self.repository.save_post_batch(posts)

        latest = await self.repository.find_latest_posts(board_id=board_id, page=page, limit=limit)

        return {"saved_count": saved_count, "items": latest}