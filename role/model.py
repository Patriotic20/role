from typing import List
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, func

from core.database.base import Base

class Role(Base):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(), # Автоматическое обновление времени при UPDATE
        nullable=False,
    )
    
    # Рекомендуется типизация Mapped[List["..."]] для Many-to-Many
    users: Mapped[List["User"]] = relationship(
        "User",
        secondary="user_role",
        back_populates="roles"
    )
    
    # Исправлено имя связи на plural (permissions) и back_populates
    permissions: Mapped[List["Permission"]] = relationship(
        "Permission",
        secondary="role_permission",
        back_populates="roles" # Проверьте, что в Permission это поле называется 'roles'
    )