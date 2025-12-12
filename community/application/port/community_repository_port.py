from abc import ABC, abstractmethod
from typing import List

from community.domain.value_object.community_post import CommunityPost


class CommunityRepositoryPort(ABC):

    @abstractmethod
    async def save_post_batch(self, posts: List[CommunityPost]) -> int:
        """새로 insert 된 개수 반환"""
        ...

    @abstractmethod
    async def find_latest_posts(self, board_id: str, page: int = 1, limit: int = 20) -> List[CommunityPost]:
        """DB에서 최신 글 조회"""
        ...