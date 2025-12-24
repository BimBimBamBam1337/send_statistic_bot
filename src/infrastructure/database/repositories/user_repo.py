from sqlalchemy import select, delete, update
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

    async def get_by_name(self, name: str) -> UserDomain | None:
        result = await self.session.execute(select(UserORM).where(UserORM.name == name))
        user_orm: UserORM | None = result.scalar_one_or_none()
        return user_orm.to_domain() if user_orm else None

    async def get_all(self) -> list[UserDomain]:
        result = await self.session.execute(select(UserORM))
        users_orm = result.scalars().all()
        return [user_orm.to_domain() for user_orm in users_orm]

    async def update(self, *, id: int, username: str | None) -> UserDomain | None:
        values = {}
        if username is not None:
            values["username"] = username
        result = await self.session.execute(
            update(UserORM).values(**values).where(UserORM.id == id).returning(UserORM)
        )
        user_orm: UserORM | None = result.scalar_one_or_none()
        return user_orm.to_domain() if user_orm else None

    async def delete(self, id: int) -> UserDomain | None:
        result = await self.session.execute(
            delete(UserORM).where(UserORM.id == id).returning(UserORM)
        )
        await self.session.flush()
        user_orm: UserORM | None = result.scalar_one_or_none()
        return user_orm.to_domain() if user_orm else None
