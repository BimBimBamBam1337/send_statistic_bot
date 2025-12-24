from datetime import datetime

from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from sqlalchemy import (
    INT,
    BIGINT,
    BOOLEAN,
    String,
    TIMESTAMP,
    func,
)

from src.domain.models import ChannelDomain, UserDomain, ExcelTableDomain


__all__ = ["BaseORM", "UserORM", "ChannelORM", "ExcelTableORM"]


BaseORM = declarative_base()


class UserORM(BaseORM):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    username: Mapped[str] = mapped_column(String, server_default="")
    is_admin: Mapped[bool] = mapped_column(BOOLEAN)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    def to_domain(self) -> UserDomain:
        return UserDomain.model_validate(self)


class ChannelORM(BaseORM):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    name: Mapped[str] = mapped_column(String, server_default="")
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    def to_domain(self) -> ChannelDomain:
        return ChannelDomain.model_validate(self)


class ExcelTableORM(BaseORM):
    __tablename__ = "excel_tabels"
    id: Mapped[int] = mapped_column(INT, primary_key=True)
    sheet_id: Mapped[str] = mapped_column(String, server_default="")
    sheet_url: Mapped[str] = mapped_column(String, server_default="")
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    def to_domain(self) -> ExcelTableDomain:
        return ExcelTableDomain.model_validate(self)
