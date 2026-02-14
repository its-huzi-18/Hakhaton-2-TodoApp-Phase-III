# Hakathon2 Phase III
AI-Powered Todo Chatbot

## Project Overview
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
- **AI**: OpenAI Agents SDK integration
- **Database**: PostgreSQL storing all tasks and conversation history

## Deployment
This application is designed for deployment on Vercel (frontend) and a cloud platform supporting FastAPI (backend).

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

## Requirements
- Server must be stateless, storing all state in DB
- Implements /frontend for chat UI, /backend for MCP server, /specs for tools
- Follows all features from Phase II and Phase 03
