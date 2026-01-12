from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from .repository import PermissionRepository, get_permission_repo
from .schema import (
    PermissionCreateRequest,
    PermissionCreateResponse,
    PermissionListRequest,
    PermissionListResponse,
)

router = APIRouter(
    tags=["Permission"],
    prefix="/permissions"
)


@router.post(
    "/",
    response_model=PermissionCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_permission(
    data: PermissionCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    repo: PermissionRepository = Depends(get_permission_repo),
) -> PermissionCreateResponse:
    return await repo.permission_create(session=session, data=data)


@router.get(
    "",
    response_model=PermissionListResponse,
)
async def list_permission(
    data: PermissionListRequest = Depends(),
    session: AsyncSession = Depends(db_helper.session_getter),
    repo: PermissionRepository = Depends(get_permission_repo),
):
    return await repo.list_permission(session=session, data=data)


@router.get(
    "/{permission_id}",
    response_model=PermissionCreateResponse,
)
async def get_permission(
    permission_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    repo: PermissionRepository = Depends(get_permission_repo),
):
    return await repo.get_permission(session=session, permission_id=permission_id)


@router.put(
    "/{permission_id}",
    response_model=PermissionCreateResponse,
)
async def update_permission(
    permission_id: int,
    data: PermissionCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    repo: PermissionRepository = Depends(get_permission_repo),
):
    return await repo.update_permission(
        session=session, 
        permission_id=permission_id, 
        data=data
    )


@router.delete(
    "/{permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_permission(
    permission_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    repo: PermissionRepository = Depends(get_permission_repo),
):
    await repo.delete_permission(session=session, permission_id=permission_id)
    return None