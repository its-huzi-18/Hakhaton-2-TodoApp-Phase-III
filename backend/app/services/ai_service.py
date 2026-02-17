"""
AI Service for Phase III - Simplified version
Handles task management with keyword-based natural language processing
Uses MCP tools for task operations
"""

import os
from typing import Dict, Any, List, Optional


class AIService:
    """AI Service with keyword-based task management using MCP tools"""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    async def process_natural_language_request(
        self,
        user_message: str,
        user_id: int,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        db_session=None
    ) -> Dict[str, Any]:
        """Process user's message and execute appropriate action using MCP tools"""
        from app.services.mcp_tool_wrappers import get_mcp_tools_wrapper
        
        wrapper = get_mcp_tools_wrapper(db_session)
        response_payload = {
            "response": "",
            "tool_calls": [],
            "task_updates": []
        }

        user_lower = user_message.lower()
        
        # Detect intent and execute MCP tool
        if any(kw in user_lower for kw in ["add task", "create task", "new task", "remember to", "i need to", "add "]):
            # Extract title
            title = user_message
            for kw in ["add task", "create task", "new task", "remember to", "i need to", "add "]:
                if kw in user_lower:
                    idx = user_lower.find(kw)
                    title = user_message[idx + len(kw):].strip().rstrip(".")
                    break

            if title and len(title) > 3:
                try:
                    # Use MCP tool: add_task
                    data = await wrapper.add_task(user_id=user_id, title=title.title())
                    response_payload["tool_calls"].append({
                        "name": "add_task",
                        "arguments": {"title": title.title(), "user_id": user_id},
                        "response": data
                    })
                    response_payload["task_updates"].append({"action": "create", "task": data})
                    response_payload["response"] = f"Added task: {data.get('title', 'New task')}"
                    return response_payload
                except Exception as e:
                    response_payload["response"] = f"Error creating task: {str(e)}"
                    return response_payload
        
        elif any(kw in user_lower for kw in ["list tasks", "show tasks", "my tasks", "get tasks", "what tasks", "all tasks"]):
            try:
                status = "all"
                if "completed" in user_lower:
                    status = "completed"
                elif "pending" in user_lower or "incomplete" in user_lower:
                    status = "pending"
                
                # Use MCP tool: list_tasks
                tasks = await wrapper.list_tasks(user_id=user_id, status=status)
                response_payload["tool_calls"].append({
                    "name": "list_tasks",
                    "arguments": {"user_id": user_id, "status": status},
                    "response": tasks
                })
                
                if not tasks:
                    response_payload["response"] = "You have no tasks"
                else:
                    status_text = status if status != "all" else "total"
                    response_payload["response"] = f"Here are your {len(tasks)} {status_text} task(s):\n\n" + "\n".join([
                        f"{'[X]' if t.get('completed') else '[ ]'} {t.get('title')}"
                        for t in tasks[:10]
                    ])
                response_payload["task_updates"].append({"action": "list", "tasks": tasks})
                return response_payload
            except Exception as e:
                response_payload["response"] = f"Error getting tasks: {str(e)}"
                return response_payload
        
        elif any(kw in user_lower for kw in ["complete task", "mark done", "mark completed", "finish task"]):
            response_payload["response"] = "To complete a task, please provide the task ID or title. For example: 'complete task 3' or 'complete task Buy groceries'"
            return response_payload
        
        elif any(kw in user_lower for kw in ["delete task", "remove task"]):
            response_payload["response"] = "To delete a task, please provide the task ID or title. For example: 'delete task 3' or 'delete task Buy groceries'"
            return response_payload
        
        else:
            # General conversation
            response_payload["response"] = """I'm your AI task assistant! I can help you:
- Add tasks: "Add task to buy groceries"
- List tasks: "Show my tasks" or "Show completed tasks"
- Complete tasks: "Complete task 3"
- Delete tasks: "Delete task 3"

What would you like to do?"""
            return response_payload


# Singleton instance
_ai_service_instance = None

def get_ai_service() -> AIService:
    """Returns the singleton AI service instance"""
    global _ai_service_instance
    if _ai_service_instance is None:
        _ai_service_instance = AIService()
    return _ai_service_instance
