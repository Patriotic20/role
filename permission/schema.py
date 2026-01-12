from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List, Optional


class PermissionCreateRequest(BaseModel):
    name: str

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        if value is None or not str(value).strip():
            raise ValueError("Permission name must not be empty")
        return value.strip().lower()


class PermissionCreateResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class PermissionListRequest(BaseModel):
    page: int
    limit: int
    name: Optional[str] = None

    @field_validator("page", "limit")
    @classmethod
    def validate_pagination(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Must be greater than 0")
        return value

    @field_validator("name", mode="before")
    @classmethod
    def normalize_filter_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip().lower()

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.limit


class PermissionListResponse(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int
    permissions: List[PermissionCreateResponse]
