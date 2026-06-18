from pydantic import BaseModel, field_validator

from typing import Optional

from datetime import datetime

import uuid





class UserLogin(BaseModel):

    username: str

    password: str





class ArticleCreate(BaseModel):

    title: str

    content: str = ""

    topic: str = ""

    is_published: bool = True

    is_pinned: bool = False



    @field_validator("title")

    @classmethod

    def title_not_empty(cls, v):

        if not v.strip():

            raise ValueError("标题不能为空")

        return v.strip()





class ArticleUpdate(BaseModel):

    title: Optional[str] = None

    content: Optional[str] = None

    topic: Optional[str] = None

    is_published: Optional[bool] = None

    is_pinned: Optional[bool] = None

    expected_updated_at: Optional[datetime] = None



    @field_validator("title")

    @classmethod

    def title_not_empty(cls, v):

        if v is not None and not v.strip():

            raise ValueError("标题不能为空")

        return v.strip() if v else v





class ArticleOut(BaseModel):

    id: uuid.UUID

    title: str

    content: str

    topic: str

    is_published: bool

    is_pinned: bool

    views: int

    created_at: datetime

    updated_at: datetime



    class Config:

        from_attributes = True





class ArticleSummaryOut(BaseModel):

    id: uuid.UUID

    title: str

    topic: str

    is_published: bool

    is_pinned: bool

    views: int

    created_at: datetime

    updated_at: datetime

    snippet: Optional[str] = None



    class Config:

        from_attributes = True





class ArticleListOut(BaseModel):

    items: list[ArticleSummaryOut]

    total: int

    page: int

    page_size: int

    has_more: bool





class TopicOut(BaseModel):

    name: str

    count: int





class Token(BaseModel):

    access_token: str

    token_type: str = "bearer"





class UploadOut(BaseModel):

    type: str

    filename: str

    url: str

    original_url: str

    compressed_url: Optional[str] = None

    size: int

