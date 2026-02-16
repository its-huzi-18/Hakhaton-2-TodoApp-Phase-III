"""
Chatbot routes for Phase III - AI-powered chat interface
Endpoint: POST /api/{user_id}/chat
"""

from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import (
    ChatMessage,
    ChatMessageCreate,
    ChatMessageRead,
    ChatRequest,
    Conversation,
    ConversationRead,
    ToolCallResponse,
    TaskUpdateResponse,
)
from app.services.chat_service import get_chat_service

router = APIRouter(prefix="/api", tags=["Chatbot"])


@router.post("/{user_id}/chat", response_model=ChatMessageRead)
async def chat_with_bot(
    user_id: str,
    user_message: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Send a message to the AI chatbot and receive a response.
    Endpoint: POST /api/{user_id}/chat
    """
    # Validate user_id format
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user ID format: {user_id}. Expected a valid UUID.",
        )

    # Validate message content
    if not user_message.content.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Message content cannot be empty",
        )

    try:
        # Process message through chat service
        chat_service = get_chat_service()
        result = await chat_service.process_user_message(
            user_id=user_id,
            user_message=user_message.content,
            db_session=db,
            conversation_id=None  # Create new or use most recent conversation
        )

        # Get AI message from DB
        ai_message = result["ai_message"]

        # Format tool calls
        tool_calls = [
            ToolCallResponse(
                name=call.get("name", ""),
                arguments=call.get("arguments", {}),
                response=call.get("response", {})
            )
            for call in result.get("tool_calls", [])
        ]

        # Format task updates
        task_updates = [
            TaskUpdateResponse(
                action=update.get("action", ""),
                task=update.get("task"),
                tasks=update.get("tasks")
            )
            for update in result.get("task_updates", [])
        ]

        # Build response
        response_message = ChatMessageRead(
            id=ai_message.id,
            role=ai_message.role,
            content=ai_message.content,
            conversation_id=ai_message.conversation_id,
            created_at=ai_message.created_at,
            tool_calls=tool_calls,
            task_updates=task_updates
        )

        return response_message

    except ValueError as ve:
        print(f"ValueError in chat_with_bot: {str(ve)}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(ve)}"
        )
    except Exception as e:
        print(f"Error in chat_with_bot: {str(e)}")
        import traceback
        traceback.print_exc()
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}"
        )


@router.get("/conversations/{user_id}", response_model=List[ConversationRead])
async def get_user_conversations(
    user_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Get all conversations for a user"""
    try:
        user_uuid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format",
        )

    result = await db.execute(
        select(Conversation).where(
            Conversation.user_id == user_uuid
        ).order_by(Conversation.created_at.desc())
    )
    conversations = result.scalars().all()
    return conversations


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Delete a conversation by ID"""
    try:
        conv_uuid = UUID(conversation_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID format",
        )

    result = await db.execute(
        select(Conversation).where(Conversation.id == conv_uuid)
    )
    conversation = result.scalar_one_or_none()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    await db.delete(conversation)
    await db.commit()

