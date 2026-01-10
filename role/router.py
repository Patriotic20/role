from fastapi import APIRouter, Depends, status

from .schema import (
    RoleCreateRequest,
    RoleCreateResponse,
    RoleListRequest,
    RoleListResponse,
)

router = APIRouter(
    tags=["Role"],
    prefix="/roles",
)


@router.post(
    "/",
    response_model=RoleCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_role(
    data: RoleCreateRequest,
) -> RoleCreateResponse:
    pass


@router.get(
    "/",
    response_model=RoleListResponse,
    status_code=status.HTTP_200_OK,
)
async def list_roles(
    data: RoleListRequest = Depends(),
) -> RoleListResponse:
    pass


@router.get(
    "/{role_id}",
    response_model=RoleCreateResponse,
    status_code=status.HTTP_200_OK,
)
async def get_role(
    role_id: int,
) -> RoleCreateResponse:
    pass


@router.put(
    "/{role_id}",
    response_model=RoleCreateResponse,
    status_code=status.HTTP_200_OK,
)
async def update_role(
    role_id: int,
    data: RoleCreateRequest,
) -> RoleCreateResponse:
    pass


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_role(
    role_id: int,
) -> None:
    pass
