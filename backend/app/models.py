from datetime import datetime
from typing import Optional, List

from pydantic import EmailStr, Field
from sqlmodel import Field as SQLField, SQLModel


# Base model for common fields
class BaseModel(SQLModel):
    id: int = SQLField(default=None, primary_key=True)
    created_at: datetime = SQLField(default_factory=datetime.utcnow)


class UserBase(SQLModel):
    email: EmailStr = Field(index=True, unique=True, max_length=255)


class User(UserBase, BaseModel, table=True):
    hashed_password: str = Field(max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)


class UserRead(UserBase):
    id: int
    created_at: datetime


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)


class Task(TaskBase, BaseModel, table=True):
    user_id: int = Field(foreign_key="user.id", index=True)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: Optional[bool] = None


class TaskRead(TaskBase):
    id: int
    user_id: int
    created_at: datetime


# Chatbot models
class ChatMessageBase(SQLModel):
    role: str  # 'user' or 'assistant'
    content: str
    conversation_id: int = Field(foreign_key="conversation.id", index=True)


class ChatMessage(ChatMessageBase, BaseModel, table=True):
    pass


class ChatMessageCreate(ChatMessageBase):
    pass


class ChatRequest(SQLModel):
    content: str


class ToolCallResponse(SQLModel):
    name: str
    arguments: dict
    response: dict | list | None = None


class TaskUpdateResponse(SQLModel):
    action: str
    task: Optional[dict] = None
    tasks: Optional[List[dict]] = None


class ChatMessageRead(ChatMessageBase):
    id: int
    created_at: datetime
    tool_calls: List[ToolCallResponse] = []
    task_updates: List[TaskUpdateResponse] = []


class ConversationBase(SQLModel):
    title: str = Field(default="New Conversation")
    user_id: int = Field(foreign_key="user.id", index=True)


class Conversation(ConversationBase, BaseModel, table=True):
    pass


class ConversationCreate(ConversationBase):
    pass


class ConversationRead(ConversationBase):
    id: int
    created_at: datetime
