"""
Standalone MCP Server using Official MCP SDK
Exposes task operations as MCP tools for AI agents
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Create MCP server instance
mcp_server = Server("todo-mcp-server")


@mcp_server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available MCP tools"""
    return [
        Tool(
            name="add_task",
            description="Create a new task in the user todo list",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID"},
                    "title": {"type": "string", "description": "Task title"},
                    "description": {"type": "string", "description": "Task description (optional)"}
                },
                "required": ["user_id", "title"]
            }
        ),
        Tool(
            name="list_tasks",
            description="Retrieve tasks for a user with optional status filter",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID"},
                    "status": {"type": "string", "enum": ["all", "pending", "completed"], "description": "Filter by status"}
                },
                "required": ["user_id"]
            }
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID"},
                    "task_id": {"type": "string", "description": "Task ID to complete"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a task from the list",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID"},
                    "task_id": {"type": "string", "description": "Task ID to delete"}
                },
                "required": ["user_id", "task_id"]
            }
        ),
        Tool(
            name="update_task",
            description="Update task title or description",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "User ID"},
                    "task_id": {"type": "string", "description": "Task ID to update"},
                    "title": {"type": "string", "description": "New title"},
                    "description": {"type": "string", "description": "New description"}
                },
                "required": ["user_id", "task_id"]
            }
        )
    ]


@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls - stub implementation"""
    # This is a stub - actual implementation connects to database
    # For now, return mock responses
    result = {"status": "success", "tool": name, "arguments": arguments}
    return [TextContent(type="text", text=json.dumps(result))]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp_server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
