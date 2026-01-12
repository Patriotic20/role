from sqlalchemy import desc, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from .model import Permission
from .schema import (
    PermissionCreateRequest,
    PermissionListRequest,
    PermissionListResponse,
)


class PermissionRepository:
    def __init__(self):
        """
        Repository is stateless; session is passed per method.
        """
        pass

    async def permission_create(
        self, session: AsyncSession, data: PermissionCreateRequest
    ) -> Permission:
        """
        Creates a new permission and returns the instance.
        """
        new_permission = Permission(**data.model_dump())

        try:
            session.add(new_permission)
            await session.commit()
            await session.refresh(new_permission)
            return new_permission
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Permission with name '{data.name}' already exists.",
            )

    async def get_permission(
        self, session: AsyncSession, permission_id: int
    ) -> Permission:
        """
        Fetches a single permission by ID or raises 404.
        """
        permission = await session.get(Permission, permission_id)

        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Permission {permission_id} not found",
            )
        return permission

    async def list_permission(
        self, session: AsyncSession, data: PermissionListRequest
    ) -> PermissionListResponse:
        """
        Returns a paginated list of permissions, newest first.
        """
        # 1. Base query for filtering
        stmt = select(Permission)

        if data.name:
            stmt = stmt.where(Permission.name.ilike(f"%{data.name}%"))

        # 2. Get total count
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await session.execute(count_stmt)
        total = total_result.scalar() or 0

        # 3. Apply Ordering (Newest First) and Pagination
        stmt = (
            stmt.order_by(desc(Permission.created_at))
            .offset(data.offset)
            .limit(data.limit)
        )

        result = await session.execute(stmt)
        permissions = result.scalars().all()

        # 4. Calculate pagination metadata
        total_pages = (total + data.limit - 1) // data.limit if total > 0 else 0

        return PermissionListResponse(
            page=data.page,
            limit=data.limit,
            total=total,
            total_pages=total_pages,
            permissions=permissions,
        )

    async def update_permission(
        self, session: AsyncSession, permission_id: int, data: PermissionCreateRequest
    ) -> Permission:
        """
        Updates an existing permission's attributes.
        """
        # Fetch existing record using the same session
        permission = await self.get_permission(session, permission_id)

        # Update attributes dynamically
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(permission, key, value)

        try:
            await session.commit()
            await session.refresh(permission)
            return permission
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Permission with name '{data.name}' already exists.",
            )

    async def delete_permission(self, session: AsyncSession, permission_id: int) -> None:
        """
        Deletes a permission by ID.
        """
        # Fetch existing record using the same session
        permission = await self.get_permission(session, permission_id)

        try:
            await session.delete(permission)
            await session.commit()
        except Exception:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not delete permission. It may be in use by a role.",
            )
            
def get_permission_repo() -> PermissionRepository:
    return PermissionRepository()