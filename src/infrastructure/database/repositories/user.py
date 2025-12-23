from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from src.database.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, is_admin: bool = False) -> User:
        user = User(id=user_id, is_admin=is_admin)
        self.session.add(user)
        await self.session.flush()
        return user

    async def get(self, user_id: int) -> User | None:
        user = await self.session.get(User, user_id)
        return user

    async def get_all(self) -> list[User] | None:
        result = await self.session.execute(select(User))
        users = result.scalars().all()
        return list(users)
