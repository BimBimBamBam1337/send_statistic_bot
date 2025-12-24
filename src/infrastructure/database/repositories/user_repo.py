from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from database.models import UserORM
from src.domain.models import UserDomain
from src.domain.repositories import AbstractUserRepository


class UserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self, *, id: int, username: str, is_admin: bool = False
    ) -> UserDomain:
        user = UserORM(id=id, is_admin=is_admin, username=username)
        self.session.add(user)
        await self.session.flush()
        return user.to_domain()

    async def get_by_id(self, id: int) -> UserDomain | None:
        result = await self.session.execute(select(UserORM).where(UserORM.id == id))
        user_orm: UserORM | None = result.scalar_one_or_none()
        return user_orm.to_domain() if user_orm else None

    async def get_all(self) -> list[UserDomain]:
        result = await self.session.execute(select(UserORM))
        users_orm = result.scalars().all()
        return [user_orm.to_domain() for user_orm in users_orm]
