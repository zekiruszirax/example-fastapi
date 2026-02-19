from pydantic import BaseModel, EmailStr, Field
from pydantic_settings import SettingsConfigDict
from datetime import datetime
from typing import Optional, Annotated

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = SettingsConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class CurrentUser(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, ge=0, le=1)]

class VoteResponse(Vote):
    user_id: int

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    owner_id: int
    owner: UserResponse
    created_at: datetime
    
    model_config = SettingsConfigDict(from_attributes=True)

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    model_config = SettingsConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None