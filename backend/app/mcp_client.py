"""
MCP Client for connecting to standalone MCP server
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from mcp import ClientSession
from mcp.client.stdio import stdio_client


class MCPClient:
    """Client for connecting to MCP server and calling tools"""
    
    def __init__(self, mcp_server_path: str = "mcp_server.py"):
        self.mcp_server_path = mcp_server_path
        self.session: Optional[ClientSession] = None
        self.context = None
    
    async def connect(self):
        """Connect to MCP server"""
        # Create stdio client context
        self.context = stdio_client(
            command="python",
            args=[self.mcp_server_path]
        )
        
        read, write = await self.context.__aenter__()
        self.session = ClientSession(read, write)
        await self.session.__aenter__()
        
        # Initialize
        await self.session.initialize()
        
        # List available tools
        tools = await self.session.list_tools()
        print(f"Connected to MCP server with tools: {[t.name for t in tools.tools]}")
    
    async def disconnect(self):
        """Disconnect from MCP server"""
        if self.session:
            await self.session.__aexit__(None, None, None)
        if self.context:
            await self.context.__aexit__(None, None, None)
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Call an MCP tool"""
        if not self.session:
            raise RuntimeError("Not connected to MCP server")
        
        result = await self.session.call_tool(tool_name, arguments)
        
        # Parse result
        if result.content:
            for item in result.content:
                if hasattr(item, 'text'):
                    return json.loads(item.text)
        
        return result
    
    async def add_task(self, user_id: str, title: str, description: str = None) -> Dict:
        """Add a task via MCP"""
        args = {"user_id": user_id, "title": title}
        if description:
            args["description"] = description
        return await self.call_tool("add_task", args)
    
    async def list_tasks(self, user_id: str, status: str = "all") -> List[Dict]:
        """List tasks via MCP"""
        args = {"user_id": user_id, "status": status}
        return await self.call_tool("list_tasks", args)
    
    async def complete_task(self, user_id: str, task_id: str) -> Dict:
        """Complete a task via MCP"""
        return await self.call_tool("complete_task", {"user_id": user_id, "task_id": task_id})
    
    async def delete_task(self, user_id: str, task_id: str) -> Dict:
        """Delete a task via MCP"""
        return await self.call_tool("delete_task", {"user_id": user_id, "task_id": task_id})
    
    async def update_task(self, user_id: str, task_id: str, title: str = None, description: str = None) -> Dict:
        """Update a task via MCP"""
        args = {"user_id": user_id, "task_id": task_id}
        if title:
            args["title"] = title
        if description:
            args["description"] = description
        return await self.call_tool("update_task", args)


# Singleton
_mcp_client = None

def get_mcp_client() -> MCPClient:
    """Get MCP client instance"""
    global _mcp_client
    if _mcp_client is None:
        _mcp_client = MCPClient()
    return _mcp_client
