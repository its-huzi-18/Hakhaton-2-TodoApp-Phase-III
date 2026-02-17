"""Debug chatbot issue"""
import asyncio
from app.db import get_db_context
from app.services.mcp_tool_wrappers import get_mcp_tools_wrapper

async def test_task_creation():
    print("Testing task creation...")
    try:
        async with get_db_context() as db:
            wrapper = get_mcp_tools_wrapper(db)
            print("Wrapper created")
            
            result = await wrapper.create_task(
                title='Test Task', 
                user_id='79a5e990-84a7-4657-9702-9666ced66643'
            )
            print(f"✅ Task created: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_task_creation())
