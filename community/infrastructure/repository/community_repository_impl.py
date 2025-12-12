from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc

from config.database.session import get_db_session
from community.application.port.community_repository_port import CommunityRepositoryPort
from community.domain.value_object.community_post import CommunityPost
from community.infrastructure.orm.community_post_orm import CommunityPostORM


class CommunityRepositoryImpl(CommunityRepositoryPort):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def get_instance(cls) -> "CommunityRepositoryImpl":
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def __init__(self):
        if not hasattr(self, "db"):
            self.db: Session = get_db_session()

    async def save_post_batch(self, posts: List[CommunityPost]) -> int:
        if not posts:
            return 0

        saved = 0
        orm_list: List[CommunityPostORM] = []

        for p in posts:
            existing = (
                self.db.query(CommunityPostORM)
                .filter(
                    and_(
                        CommunityPostORM.provider == p.provider,
                        CommunityPostORM.board_id == p.board_id,
                        CommunityPostORM.external_post_id == p.external_post_id,
                    )
                )
                .first()
            )
            if existing:
                continue

            orm_list.append(
                CommunityPostORM(
                    provider=p.provider,
                    board_id=p.board_id,
                    external_post_id=p.external_post_id,
                    title=p.title,
                    author=p.author,
                    content=p.content,
                    url=p.url,
                    view_count=p.view_count,
                    recommend_count=p.recommend_count,
                    comment_count=p.comment_count,
                    posted_at=p.posted_at,
                    fetched_at=p.fetched_at,
                )
            )

        if not orm_list:
            return 0

        self.db.add_all(orm_list)
        self.db.commit()
        saved = len(orm_list)

        return saved

    async def find_latest_posts(self, board_id: str, page: int = 1, limit: int = 20) -> List[CommunityPost]:
        offset = (page - 1) * limit

        rows = (
            self.db.query(CommunityPostORM)
            .filter(CommunityPostORM.board_id == board_id)
            .order_by(desc(CommunityPostORM.posted_at), desc(CommunityPostORM.id))
            .offset(offset)
            .limit(limit)
            .all()
        )

        return [
            CommunityPost(
                provider=r.provider,
                board_id=r.board_id,
                external_post_id=r.external_post_id,
                title=r.title,
                author=r.author or "",
                content=r.content or "",
                url=r.url,
                view_count=r.view_count,
                recommend_count=r.recommend_count,
                comment_count=r.comment_count or 0,
                posted_at=r.posted_at,
                fetched_at=r.fetched_at,
            )
            for r in rows
        ]