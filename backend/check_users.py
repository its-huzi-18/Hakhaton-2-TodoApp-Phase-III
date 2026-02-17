"""Check user IDs in database"""
import asyncio
from app.db import engine, get_db
from app.models import User
from sqlmodel import select

async def check_users():
    async with engine.begin() as conn:
        result = await conn.execute(select(User).limit(5))
        users = result.fetchall()
        print("Users in database:")
        for row in users:
            user = row[0]
            print(f"  ID: {user.id} (type: {type(user.id).__name__})")
            print(f"  Email: {user.email}")
            print()

if __name__ == "__main__":
    asyncio.run(check_users())
