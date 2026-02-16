"""
AI Service using OpenAI Agents SDK for Phase III
Handles task management with MCP tools via OpenAI Agents framework
"""

import os
import json
import re
from typing import Dict, Any, List, Optional
from uuid import UUID

from dotenv import load_dotenv
from agents import Agent, Runner
from agents.run import RunConfig

load_dotenv()


def safe_uuid(val: Optional[str]) -> Optional[UUID]:
    """Convert string to UUID safely"""
    if val is None:
        return None
    try:
        return UUID(val)
    except (ValueError, TypeError):
        return val


class AIService:
    """AI Service using OpenAI Agents SDK"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        
        if not self.api_key:
            print("⚠️ OPENAI_API_KEY not set. AI functionality will be limited.")
            self.agent = None
        else:
            self.agent = None

    def _get_system_prompt(self) -> str:
        return """
You are a helpful AI assistant for a todo task management application.
You can help users manage their tasks through natural conversation.

CAPABILITIES:
- Add new tasks to the user's todo list
- List tasks (all, pending, or completed)
- Mark tasks as complete
- Delete tasks
- Update task titles and descriptions

GUIDELINES:
- Be friendly and conversational
- Always confirm actions you take
- If the user's request is ambiguous, ask for clarification
- When showing tasks, format them in a readable way
- Use emojis appropriately to make responses engaging
"""

    async def process_natural_language_request(
        self,
        user_message: str,
        user_id: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        db_session=None
    ) -> Dict[str, Any]:
        """Process user's natural language request using OpenAI Agents SDK"""
        from app.services.mcp_tool_wrappers import get_mcp_tools_wrapper
        
        response_payload = {
            "response": "",
            "tool_calls": [],
            "task_updates": []
        }
        
        if not self.api_key:
            return {
                "response": "⚠️ AI service not configured. Please set OPENAI_API_KEY.",
                "tool_calls": [],
                "task_updates": []
            }
        
        wrapper = get_mcp_tools_wrapper(db_session)
        
        # Create agent with system prompt
        agent = Agent(
            name="TodoAssistant",
            instructions=self._get_system_prompt(),
            model=self.model_name,
        )
        
        try:
            # Run the agent
            run_config = RunConfig(
                model=self.model_name,
                tracing_disabled=True
            )
            
            result = await Runner.run(
                agent,
                input=user_message,
                run_config=run_config
            )
            
            ai_response = result.final_output.strip()
            
            # Parse response for tool calls
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                try:
                    parsed = json.loads(json_match.group())
                    if isinstance(parsed, dict) and "tool_name" in parsed:
                        tool_name = parsed["tool_name"]
                        arguments = parsed.get("arguments", {})
                        
                        if tool_name in ["create_task", "get_tasks", "find_task_by_title"] and "user_id" not in arguments:
                            arguments["user_id"] = user_id
                        
                        if hasattr(wrapper, tool_name):
                            data = await getattr(wrapper, tool_name)(**arguments)
                            response_payload["tool_calls"].append({
                                "name": tool_name,
                                "arguments": arguments,
                                "response": data
                            })
                            
                            if "create" in tool_name:
                                response_payload["response"] = f"✅ Task added: {data.get('title', 'New task')}"
                            elif "delete" in tool_name:
                                response_payload["response"] = "🗑️ Task deleted successfully"
                            elif "complete" in tool_name:
                                response_payload["response"] = "✅ Task marked as completed"
                            elif "update" in tool_name:
                                response_payload["response"] = "✏️ Task updated successfully"
                            elif "get" in tool_name:
                                tasks = data if isinstance(data, list) else []
                                if not tasks:
                                    response_payload["response"] = "📋 You have no tasks"
                                else:
                                    response_payload["response"] = f"📋 Here are your {len(tasks)} task(s)"
                            else:
                                response_payload["response"] = ai_response
                            return response_payload
                except json.JSONDecodeError:
                    pass
            
            # Fallback: semantic parsing
            user_lower = user_message.lower()
            if any(kw in user_lower for kw in ["add task", "create task", "new task", "remember to", "i need to"]):
                title = user_message
                for kw in ["add task", "create task", "new task", "remember to", "i need to"]:
                    if kw in user_lower:
                        idx = user_lower.find(kw)
                        title = user_message[idx + len(kw):].strip().rstrip(".")
                        break
                
                if title and len(title) > 3:
                    data = await wrapper.create_task(title=title.title(), user_id=user_id)
                    response_payload["tool_calls"].append({
                        "name": "create_task",
                        "arguments": {"title": title.title(), "user_id": user_id},
                        "response": data
                    })
                    response_payload["task_updates"].append({"action": "create", "task": data})
                    response_payload["response"] = f"✅ Added task: {title.title()}"
                    return response_payload
            
            response_payload["response"] = ai_response if ai_response else "I'm here to help you manage your tasks."
            return response_payload
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                "response": f"⚠️ Error: {str(e)}",
                "tool_calls": [],
                "task_updates": []
            }


_ai_service_instance = None

def get_ai_service() -> AIService:
    """Returns the singleton AI service instance"""
    global _ai_service_instance
    if _ai_service_instance is None:
        _ai_service_instance = AIService()
    return _ai_service_instance
