"""Recreate task table with correct schema"""
import asyncio
from sqlalchemy import text
from app.db import engine

async def recreate_task_table():
    print("Recreating task table with correct schema...")
    async with engine.begin() as conn:
        # Drop existing table
        print("Dropping existing task table...")
        await conn.execute(text("DROP TABLE IF EXISTS task CASCADE"))
        print("Table dropped")
        
        # Create new table with correct schema
        print("Creating new task table...")
        await conn.execute(text("""
            CREATE TABLE task (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                title VARCHAR(200) NOT NULL,
                description VARCHAR(1000),
                is_completed BOOLEAN DEFAULT FALSE,
                user_id UUID NOT NULL REFERENCES \"user\"(id)
            )
        """))
        print("Task table created!")
        
        # Create index
        await conn.execute(text("CREATE INDEX idx_task_user_id ON task(user_id)"))
        print("Index created!")
    
    print("\nTask table recreated successfully!")

if __name__ == "__main__":
    asyncio.run(recreate_task_table())
