#!/usr/bin/env python3
"""
System test for the Todo AI Chatbot
This script verifies that all components of the system work together correctly.
"""

import asyncio
import os
import sys
from uuid import uuid4

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models import User, Task, Conversation, ChatMessage
from app.db import init_db
from app.services.chat_service import get_chat_service
from app.services.ai_service import get_ai_service


async def test_system():
    """Test the complete Todo AI Chatbot system"""
    
    print("Starting Todo AI Chatbot system test...")
    
    # Setup database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test_todo_app.db")
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    # Initialize database
    await init_db()
    
    print("Database initialized")
    
    # Create a test user
    user_id = str(uuid4())
    print(f"Created test user with ID: {user_id}")
    
    # Test the AI service directly
    print("Testing AI service...")
    ai_service = get_ai_service()
    
    # Mock a database session for testing
    async with async_session() as session:
        # Test 1: Add a task
        print("Testing task creation...")
        result = await ai_service.process_natural_language_request(
            user_message="Add buy groceries to my todo list",
            user_id=user_id,
            db_session=session
        )
        
        print(f"Response: {result['response']}")
        print(f"Tool calls: {len(result['tool_calls'])}")
        print(f"Task updates: {len(result['task_updates'])}")
        
        if result['tool_calls']:
            print("Task creation successful")
        else:
            print("Task creation failed")
            
        # Test 2: Show tasks
        print("Testing task listing...")
        result = await ai_service.process_natural_language_request(
            user_message="Show me my tasks",
            user_id=user_id,
            db_session=session
        )
        
        print(f"Response: {result['response']}")
        print(f"Tool calls: {len(result['tool_calls'])}")
        
        if result['tool_calls']:
            print("Task listing successful")
        else:
            print("Task listing failed")
            
        # Test 3: Complete a task
        print("Testing task completion...")
        result = await ai_service.process_natural_language_request(
            user_message="Complete the first task",
            user_id=user_id,
            db_session=session
        )
        
        print(f"Response: {result['response']}")
        print(f"Tool calls: {len(result['tool_calls'])}")
        
        if result['tool_calls']:
            print("Task completion successful")
        else:
            print("Task completion failed")
    
    print("System test completed!")


if __name__ == "__main__":
    asyncio.run(test_system())