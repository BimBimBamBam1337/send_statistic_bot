from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
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

    sheet_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("excel_tabels.sheet_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    excel_table: Mapped["ExcelTableORM"] = relationship(
        "ExcelTableORM",
        back_populates="channel",
        uselist=False,
    )

    def to_domain(self) -> ChannelDomain:
        return ChannelDomain.model_validate(self)


class ExcelTableORM(BaseORM):
    __tablename__ = "excel_tabels"

    id: Mapped[int] = mapped_column(INT, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, server_default="")
    sheet_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    sheet_url: Mapped[str] = mapped_column(String, server_default="")
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    channel: Mapped["ChannelORM"] = relationship(
        "ChannelORM",
        back_populates="excel_table",
        uselist=False,
    )

    def to_domain(self) -> ExcelTableDomain:
        return ExcelTableDomain.model_validate(self)
