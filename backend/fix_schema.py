"""Fix database schema - add missing columns"""
import asyncio
from sqlalchemy import text
from app.db import engine

async def fix_schema():
    print("Fixing database schema...")
    async with engine.begin() as conn:
        # Check if is_completed column exists
        result = await conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'task' AND column_name = 'is_completed'
        """))
        row = result.fetchone()
        
        if not row:
            print("Adding is_completed column to task table...")
            await conn.execute(text("""
                ALTER TABLE task 
                ADD COLUMN is_completed BOOLEAN DEFAULT FALSE
            """))
            print("Added is_completed column!")
        else:
            print("is_completed column already exists")
        
        # Check for description column
        result = await conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'task' AND column_name = 'description'
        """))
        row = result.fetchone()
        
        if not row:
            print("Adding description column to task table...")
            await conn.execute(text("""
                ALTER TABLE task 
                ADD COLUMN description VARCHAR(1000)
            """))
            print("Added description column!")
        else:
            print("description column already exists")
    
    print("\nDatabase schema fixed!")

if __name__ == "__main__":
    asyncio.run(fix_schema())
