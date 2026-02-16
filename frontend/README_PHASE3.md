# Phase III: Todo AI Chatbot

AI-powered chatbot interface for managing todos through natural language using MCP (Model Context Protocol) server architecture, OpenAI Agents SDK, and Official MCP SDK.

## Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | Next.js 16 + React |
| Backend | Python FastAPI |
| AI Framework | OpenAI Agents SDK |
| MCP Server | Official MCP SDK (standalone) |
| ORM | SQLModel |
| Database | Neon Serverless PostgreSQL |
| Authentication | Better Auth / JWT |

## Architecture

Frontend -> FastAPI (/api/{user_id}/chat) -> OpenAI Agents SDK -> MCP Client -> MCP Server -> Database

## Setup Instructions

### Backend

1. cd backend
2. pip install -r requirements.txt
3. Create .env with DATABASE_URL, OPENAI_API_KEY, JWT_SECRET_KEY
4. python -m uvicorn app.main:app --reload
5. (Optional) python mcp_server.py (separate terminal)

### Frontend

1. npm install
2. Create .env.local with NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
3. npm run dev

## API Endpoint

POST /api/{user_id}/chat
Request: {"content": "Add a task to buy groceries"}
Response: {"response": "Task added", "conversation_id": "uuid", "tool_calls": [...]}

## MCP Tools

- add_task: Create a new task
- list_tasks: Retrieve tasks (filter by status)
- complete_task: Mark task complete
- delete_task: Remove a task
- update_task: Modify task

## Compliance

[x] OpenAI Agents SDK
[x] Official MCP SDK
[x] Standalone MCP server
[x] Stateless architecture
[x] Database persistence
[x] Natural language commands
