from datetime import datetime

from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from sqlalchemy import (
    BIGINT,
    BOOLEAN,
    String,
    TIMESTAMP,
    func,
)


__all__ = ["Base", "User"]


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    username: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(BOOLEAN)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())


class Chanel(Base):
    __tablename__ = "chanels"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    title: Mapped[str] = mapped_column(String, server_default="")
    channel_added_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )


class ExcelTable(Base):
    __tablename__ = "excel_tabels"
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    title: Mapped[str] = mapped_column(String, server_default="")

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
