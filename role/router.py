from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from .repository import get_user_repo, UserRepository
from .schema import (
    RoleCreateRequest,
    RoleCreateResponse,
    RoleListRequest,
    RoleListResponse,
)

router = APIRouter(tags=["Role"], prefix="/roles")

@router.post("/", response_model=RoleCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    data: RoleCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    repo: UserRepository = Depends(get_user_repo)
):
    return await repo.create_role(session=session, data=data)

@router.get("/", response_model=RoleListResponse)
async def list_roles(
    data: RoleListRequest = Depends(),
    session: AsyncSession = Depends(db_helper.session_getter),
    repo: UserRepository = Depends(get_user_repo)
):
    return await repo.list_role(session=session, data=data)

@router.get("/{role_id}", response_model=RoleCreateResponse)
async def get_role(
    role_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    repo: UserRepository = Depends(get_user_repo)
):
    return await repo.get_role(session=session, role_id=role_id)

@router.put("/{role_id}", response_model=RoleCreateResponse)
async def update_role(
    role_id: int,
    data: RoleCreateRequest,
    session: AsyncSession = Depends(db_helper.session_getter),
    repo: UserRepository = Depends(get_user_repo)
):
    return await repo.update_role(session=session, role_id=role_id, data=data)

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    session: AsyncSession = Depends(db_helper.session_getter),
    repo: UserRepository = Depends(get_user_repo)
):
    await repo.delete_role(session=session, role_id=role_id)