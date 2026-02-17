"""
MCP Tool Wrappers for Phase III
Exposes task operations as MCP tools for AI agents
"""

from typing import Dict, Any, List, Optional


class MCPToolWrappers:
    """
    Wrapper class that exposes Phase II functionality as MCP tools
    for AI agents to use when processing natural language commands.
    """

    def __init__(self, db_session):
        self.db = db_session
        from app.services.task_service import get_task_service
        self.task_service = get_task_service(db_session)

    async def add_task(self, user_id: int, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        MCP Tool: Create a new task
        
        Args:
            user_id: The ID of the user creating the task
            title: The title of the task
            description: Optional description of the task

        Returns:
            Dictionary with task_id, status, title
        """
        from app.models import TaskCreate
        from sqlmodel import select, func
        
        # Get max ID to generate next integer ID
        result = await self.db.execute(select(func.max(self.task_service.model.id)))
        max_id = result.scalar()
        new_id = (max_id or 0) + 1
        
        task_create_data = TaskCreate(
            title=title,
            description=description,
            is_completed=False
        )
        
        # Use task service but override ID
        created_task = await self.task_service.create_task_with_id(task_create_data, user_id, new_id)
        
        return {
            "task_id": created_task.id,
            "status": "created",
            "title": created_task.title
        }

    async def list_tasks(self, user_id: int, status: Optional[str] = "all") -> List[Dict[str, Any]]:
        """
        MCP Tool: Retrieve tasks from the list
        
        Args:
            user_id: The ID of the user whose tasks to retrieve
            status: Filter for completion status ("all", "pending", "completed")

        Returns:
            Array of task objects
        """
        is_completed = None
        if status == "pending":
            is_completed = False
        elif status == "completed":
            is_completed = True
        # "all" or None returns all tasks
        
        tasks = await self.task_service.get_tasks(user_id, is_completed)
        
        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.is_completed
            }
            for task in tasks
        ]

    async def complete_task(self, user_id: int, task_id: int) -> Dict[str, Any]:
        """
        MCP Tool: Mark a task as complete
        
        Args:
            user_id: The ID of the user
            task_id: The ID of the task to mark as completed

        Returns:
            Dictionary with task_id, status, title
        """
        from app.models import TaskUpdate
        
        task_update_data = TaskUpdate(is_completed=True)
        updated_task = await self.task_service.update_task(task_id, task_update_data, user_id)
        
        if updated_task is None:
            return {"task_id": task_id, "status": "not_found", "error": "Task not found"}
        
        return {
            "task_id": task_id,
            "status": "completed",
            "title": updated_task.title
        }

    async def delete_task(self, user_id: int, task_id: int) -> Dict[str, Any]:
        """
        MCP Tool: Remove a task from the list
        
        Args:
            user_id: The ID of the user
            task_id: The ID of the task to delete

        Returns:
            Dictionary with task_id, status, title
        """
        # Get task info before deletion
        from app.models import Task
        from sqlmodel import select
        
        result = await self.db.execute(select(Task).where(Task.id == task_id, Task.user_id == user_id))
        task = result.scalar_one_or_none()
        
        if not task:
            return {"task_id": task_id, "status": "not_found", "error": "Task not found"}
        
        task_title = task.title
        success = await self.task_service.delete_task(task_id, user_id)
        
        if success:
            return {"task_id": task_id, "status": "deleted", "title": task_title}
        else:
            return {"task_id": task_id, "status": "error", "error": "Failed to delete"}

    async def update_task(self, user_id: int, task_id: int, 
                         title: Optional[str] = None, 
                         description: Optional[str] = None) -> Dict[str, Any]:
        """
        MCP Tool: Modify task title or description
        
        Args:
            user_id: The ID of the user
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            Dictionary with task_id, status, title
        """
        from app.models import TaskUpdate
        
        task_update_data = TaskUpdate(
            title=title,
            description=description
        )
        
        updated_task = await self.task_service.update_task(task_id, task_update_data, user_id)
        
        if updated_task is None:
            return {"task_id": task_id, "status": "not_found", "error": "Task not found"}
        
        return {
            "task_id": task_id,
            "status": "updated",
            "title": updated_task.title
        }


# MCP Tools definitions for OpenAI Agents SDK
MCP_TOOLS_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task in the user's todo list",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "The ID of the user creating the task"},
                    "title": {"type": "string", "description": "The title of the task"},
                    "description": {"type": "string", "description": "Optional description of the task"}
                },
                "required": ["user_id", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Retrieve tasks from the list",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "The ID of the user whose tasks to retrieve"},
                    "status": {"type": "string", "description": "Filter: 'all', 'pending', or 'completed'", "enum": ["all", "pending", "completed"]}
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as complete",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "The ID of the user"},
                    "task_id": {"type": "integer", "description": "The ID of the task to mark as completed"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Remove a task from the list",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "The ID of the user"},
                    "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Modify task title or description",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer", "description": "The ID of the user"},
                    "task_id": {"type": "integer", "description": "The ID of the task to update"},
                    "title": {"type": "string", "description": "New title for the task"},
                    "description": {"type": "string", "description": "New description for the task"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    }
]


def get_mcp_tools_wrapper(db_session):
    """Factory function to create an instance of MCPToolWrappers"""
    return MCPToolWrappers(db_session)
