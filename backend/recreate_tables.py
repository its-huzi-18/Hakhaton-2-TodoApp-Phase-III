"""Recreate all tables with correct integer ID schema"""
import asyncio
from sqlalchemy import text
from app.db import engine

async def recreate_all_tables():
    print("Recreating database tables with integer IDs...")
    async with engine.begin() as conn:
        # Drop existing tables in correct order (foreign keys)
        print("Dropping existing tables...")
        await conn.execute(text("DROP TABLE IF EXISTS chat_message CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS conversation CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS task CASCADE"))
        await conn.execute(text("DROP TABLE IF EXISTS \"user\" CASCADE"))
        print("Tables dropped")
        
        # Create user table
        print("Creating user table...")
        await conn.execute(text("""
            CREATE TABLE "user" (
                id SERIAL PRIMARY KEY,
                created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                email VARCHAR(255) NOT NULL UNIQUE,
                hashed_password VARCHAR(255) NOT NULL
            )
        """))
        await conn.execute(text("CREATE INDEX idx_user_email ON \"user\"(email)"))
        print("User table created")
        
        # Create task table
        print("Creating task table...")
        await conn.execute(text("""
            CREATE TABLE task (
                id SERIAL PRIMARY KEY,
                created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                title VARCHAR(200) NOT NULL,
                description VARCHAR(1000),
                is_completed BOOLEAN DEFAULT FALSE,
                user_id INTEGER NOT NULL REFERENCES "user"(id)
            )
        """))
        await conn.execute(text("CREATE INDEX idx_task_user_id ON task(user_id)"))
        print("Task table created")
        
        # Create conversation table
        print("Creating conversation table...")
        await conn.execute(text("""
            CREATE TABLE conversation (
                id SERIAL PRIMARY KEY,
                created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                title VARCHAR(255) DEFAULT 'New Conversation',
                user_id INTEGER NOT NULL REFERENCES "user"(id)
            )
        """))
        await conn.execute(text("CREATE INDEX idx_conversation_user_id ON conversation(user_id)"))
        print("Conversation table created")
        
        # Create chat_message table
        print("Creating chat_message table...")
        await conn.execute(text("""
            CREATE TABLE chat_message (
                id SERIAL PRIMARY KEY,
                created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                role VARCHAR(50) NOT NULL,
                content TEXT NOT NULL,
                conversation_id INTEGER NOT NULL REFERENCES conversation(id)
            )
        """))
        await conn.execute(text("CREATE INDEX idx_chat_message_conversation_id ON chat_message(conversation_id)"))
        print("Chat message table created")
    
    print("\n✅ All tables recreated with integer IDs!")

if __name__ == "__main__":
    asyncio.run(recreate_all_tables())
