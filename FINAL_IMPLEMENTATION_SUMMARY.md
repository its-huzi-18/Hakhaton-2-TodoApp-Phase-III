# Todo AI Chatbot - Phase III

This is an AI-powered todo application featuring natural language processing for task management. The application combines FastAPI backend with MCP tools, a Next.js frontend chat UI, and PostgreSQL database storage.

## Features

- Natural language task management (add, list, update, delete, complete tasks)
- AI-powered chatbot interface
- User authentication and authorization
- Conversation history tracking
- Real-time task management

## Architecture

- **Backend**: FastAPI with MCP tools (add_task, list_tasks, update_task, delete_task, complete_task)
- **Frontend**: Next.js chat UI communicating with backend
- **AI**: OpenAI-compatible API integration (OpenRouter)
- **Database**: PostgreSQL storing all tasks and conversation history

## Components

### Backend (Python/FastAPI)

- **Models**: Implemented Conversation, Message, and TodoTask models with SQLAlchemy
- **Services**:
  - AI Service to interface with AI providers via OpenAI API
  - MCP Tool Wrappers for task management operations
  - Chat Service for handling conversation flow
- **API**:
  - Chat endpoint at `/api/users/{user_id}/chat`
  - Conversation management endpoints
  - Proper validation, error handling, and logging
- **Database**: SQLAlchemy ORM with PostgreSQL support

### Frontend (Next.js/React)

- **Components**:
  - ChatInterface: Main chat UI component
  - MessageList: Displays conversation history with formatted task responses
- **Pages**:
  - ChatPage: Main application page
- **Services**:
  - API service for backend communication

## MCP Tools

The system implements the following MCP tools for AI agent interaction:

- `create_task`: Create a new task in the user's todo list
- `get_tasks`: Retrieve tasks for a specific user
- `update_task`: Update an existing task in the user's todo list
- `delete_task`: Delete a task from the user's todo list
- `complete_task`: Mark a task as completed
- `find_task_by_title`: Find a task by its title for a specific user

## Natural Language Processing

The AI service interprets natural language commands:
- "add" triggers the `create_task` tool
- "show" triggers the `get_tasks` tool
- "complete" triggers the `complete_task` tool
- Other variations are handled through semantic parsing

## Database Schema

- **User**: Stores user information
- **Task**: Stores individual tasks with completion status
- **Conversation**: Groups related chat messages
- **ChatMessage**: Individual exchanges within a conversation

## Environment Variables

```bash
DATABASE_URL=postgresql://username:password@localhost/dbname
JWT_SECRET_KEY=your-secret-key
OPENROUTER_API_KEY=your-openrouter-api-key
AI_MODEL=mistralai/devstral-2512:free
```

## Running the Application

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Deployment

### Frontend (Vercel)
1. Clone the repository
2. Navigate to the `frontend` directory
3. Set environment variables in Vercel dashboard:
   - `NEXT_PUBLIC_API_URL`: Your backend API URL
   - `NEXT_PUBLIC_API_BASE_URL`: Your backend API base URL
4. Deploy using Vercel CLI or connect your GitHub repository

### Backend (Cloud Platform)
1. Set up a PostgreSQL database
2. Deploy the FastAPI application to your preferred cloud platform
3. Configure environment variables:
   - `DATABASE_URL`: PostgreSQL connection string
   - `OPENAI_API_KEY`: OpenAI API key
   - `ANTHROPIC_API_KEY`: Anthropic API key (if using Claude)
   - `APP_SECRET_KEY`: Secret key for JWT tokens
   - `ALLOWED_ORIGINS`: Allowed origins for CORS
4. Ensure the backend is accessible to your frontend

## Key Implementation Notes

- Server is stateless, storing all state in DB
- Implements /frontend for chat UI, /backend for MCP server, /specs for tools
- Follows all features from Phase II and Phase III requirements
- MCP tools are accessible to AI agents for natural language processing
- Conversation history is stored in the database for continuity