from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, func
from datetime import datetime


from core.database.base import Base


class Permission(Base):
    
    __tablename__ = "permissions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )
    
    
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
    
    roles = relationship(
        "Role",
        secondary="role_permission",
        back_populates="permissions"
    )