# Environment Setup Guide

## Quick Start

### 1. Backend Setup

#### Create Backend Environment File
Copy the example file and configure your environment:

```bash
cd backend
cp .env.example .env
```

#### Edit `.env` with your credentials:

```env
# Database - Local PostgreSQL
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/tododb

# JWT - Generate a secure key for production
JWT_SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256

# OpenAI API - Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini

# Application
DEBUG=True
APP_NAME=Phase III Todo API
APP_VERSION=0.1.0

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### 2. Frontend Setup

#### Create Frontend Environment File:

```bash
cd frontend
cp .env.local.example .env.local
```

#### Edit `.env.local`:

```env
# Local Development
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api

# For Production (update after deploying backend)
# NEXT_PUBLIC_API_BASE_URL=https://your-backend-api.com/api
```

## Local Development

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+

### Backend Installation

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Initialize database
# Make sure PostgreSQL is running and database exists
psql -U postgres -c "CREATE DATABASE tododb;"

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Installation

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Production Deployment

### Vercel (Frontend)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Set environment variables in Vercel dashboard:
- `NEXT_PUBLIC_API_BASE_URL` - Your deployed backend URL

3. Deploy:
```bash
cd frontend
vercel
```

### Backend Deployment Options

#### Option A: Railway
1. Create new project on Railway
2. Connect your GitHub repo
3. Set environment variables
4. Deploy

#### Option B: Render
1. Create new Web Service
2. Connect GitHub repo
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

#### Option C: AWS/GCP/Azure
Deploy using your preferred cloud provider with:
- PostgreSQL database (RDS, Cloud SQL, etc.)
- Container service or VM for the FastAPI app

### Production Environment Variables

**Backend:**
```env
DATABASE_URL=postgresql+asyncpg://user:password@production-db-host:5432/dbname
JWT_SECRET_KEY=<generate-strong-random-key>
OPENAI_API_KEY=sk-your-production-key
DEBUG=False
ALLOWED_ORIGINS=https://your-app.vercel.app
```

**Frontend:**
```env
NEXT_PUBLIC_API_BASE_URL=https://your-backend-api.com/api
```

## Testing the Chatbot

1. **Start both servers** (backend on port 8000, frontend on port 3000)

2. **Create an account** or login

3. **Navigate to Chat** (/chat)

4. **Try these commands:**
   - "Add a task to buy groceries"
   - "Show my tasks"
   - "Show my completed tasks"
   - "Complete task buy groceries"
   - "Delete task buy groceries"

## Troubleshooting

### Chatbot not responding with AI
- Check `OPENAI_API_KEY` is set correctly
- Verify API key has credits available
- Check backend logs for errors

### Database connection errors
- Ensure PostgreSQL is running
- Verify `DATABASE_URL` credentials
- Check database exists: `psql -U postgres -l`

### CORS errors
- Update `ALLOWED_ORIGINS` in backend `.env`
- Include both http and https URLs as needed
- Use comma-separated format for multiple origins

### Authentication issues
- Ensure `JWT_SECRET_KEY` is set
- Check token is being stored in localStorage
- Clear browser cache and re-login

## API Endpoints

### Authentication
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Tasks
- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks/{id}` - Get specific task
- `PATCH /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

### Chatbot
- `POST /api/{user_id}/chat` - Send message to AI
- `GET /api/conversations/{user_id}` - Get conversations
- `DELETE /api/conversations/{id}` - Delete conversation

## Security Notes

⚠️ **Important for Production:**
- Never commit `.env` files to Git
- Generate strong random `JWT_SECRET_KEY`
- Use environment-specific OpenAI API keys
- Enable HTTPS for all production deployments
- Set `DEBUG=False` in production
- Restrict `ALLOWED_ORIGINS` to your actual domains
