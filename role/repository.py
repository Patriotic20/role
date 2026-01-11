from math import ceil

from sqlalchemy import insert, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException, status

from core.logging import logging
from .schema import RoleCreateRequest, RoleListRequest, RoleListResponse
from .model import Role

class UserRepository:
    def __init__(self):
        pass

    async def create_role(self, session: AsyncSession, data: RoleCreateRequest) -> Role:
        """Создание новой роли."""
        stmt = insert(Role).values(**data.model_dump()).returning(Role)
        
        try:
            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()
            
        except IntegrityError as e:
            await session.rollback()
            logging.error(f"Integrity error during role creation: {e}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Role with these unique constraints already exists."
            ) from e

    async def get_role(self, session: AsyncSession, role_id: int) -> Role:
        """Получение одной роли по ID или 404."""
        try:
            role = await session.get(Role, role_id)
            
            if role is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Role with id {role_id} not found"
                )
            
            return role

        except HTTPException:
            raise
        except Exception as e:
            logging.error(f"Unexpected error fetching role {role_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    async def list_role(self, session: AsyncSession, data: RoleListRequest) -> RoleListResponse:
        """Получение списка ролей с фильтрацией и пагинацией."""
        try:
            # 1. Базовый запрос
            base_stmt = select(Role)
            if data.name:
                base_stmt = base_stmt.where(Role.name.ilike(f"%{data.name}%"))

            # 2. Подсчет общего количества через подзапрос (subquery)
            count_stmt = select(func.count()).select_from(base_stmt.subquery())
            total_result = await session.execute(count_stmt)
            total = total_result.scalar() or 0

            # 3. Получение данных с лимитом и смещением
            data_stmt = base_stmt.order_by(Role.id).limit(data.limit).offset(data.offset)
            result = await session.execute(data_stmt)
            roles = result.scalars().all()

            # 4. Расчет страниц
            total_pages = ceil(total / data.limit) if total > 0 else 0

            return RoleListResponse(
                page=data.page,
                limit=data.limit,
                total=total,
                total_pages=total_pages,
                roles=roles
            )

        except Exception as e:
            logging.error(f"Error fetching roles list: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error retrieving roles from database"
            )

    async def update_role(self, session: AsyncSession, role_id: int, data: RoleCreateRequest) -> Role:
        """Обновление существующей роли."""
        try:
            # Используем get_role для получения объекта и проверки на 404
            role = await self.get_role(session, role_id)
            
            # Обновляем поля
            update_data = data.model_dump()
            for key, value in update_data.items():
                setattr(role, key, value)
            
            await session.commit()
            await session.refresh(role)
            return role

        except IntegrityError as e:
            await session.rollback()
            logging.error(f"Conflict during role update: {e}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Role with this name already exists."
            )
        except HTTPException:
            raise
        except Exception as e:
            await session.rollback()
            logging.error(f"Unexpected error updating role {role_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during update"
            )

    async def delete_role(self, session: AsyncSession, role_id: int) -> bool:
        """Удаление роли."""
        try:
            role = await self.get_role(session, role_id)
            
            await session.delete(role)
            await session.commit()
            return True

        except IntegrityError as e:
            await session.rollback()
            logging.error(f"Foreign key constraint error on delete role {role_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete role: it is currently in use."
            )
        except HTTPException:
            raise
        except Exception as e:
            await session.rollback()
            logging.error(f"Unexpected error deleting role {role_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error during deletion"
            )
            
def get_user_repo() -> UserRepository:
    return UserRepository()