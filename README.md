# Hakhaton TodoApp Phase III - AI-Powered Task Management

[![Phase III](https://img.shields.io/badge/Phase-III-blue)](https://github.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-16.1-black)](https://nextjs.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-Agents-7ab8ff)](https://openai.com/)

An AI-powered todo application featuring natural language processing for task management. Built with FastAPI backend, Next.js frontend, and OpenAI Agents SDK.

## 🌟 Features

### Core Functionality
- ✅ **User Authentication** - Secure JWT-based authentication
- ✅ **Task Management** - Full CRUD operations for tasks
- ✅ **AI Chatbot** - Natural language task management
- ✅ **Conversation History** - Persistent chat history
- ✅ **Real-time Updates** - Instant feedback on all actions

### AI Capabilities
The AI assistant understands natural language and can:
- 📝 **Add tasks**: "Add a task to buy groceries"
- 📋 **List tasks**: "Show my tasks" or "Show completed tasks"
- ✅ **Complete tasks**: "Complete task Buy groceries"
- 🗑️ **Delete tasks**: "Delete task Buy groceries"
- ✏️ **Update tasks**: "Update the task description"

### Technology Stack
- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.11+, SQLModel
- **Database**: PostgreSQL with asyncpg
- **AI**: OpenAI Agents SDK (GPT-4o-mini)
- **Auth**: JWT tokens with bcrypt password hashing

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- PostgreSQL 14 or higher
- OpenAI API Key

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Hakhaton-2-TodoApp-Phase-III
```

### 2. Setup Environment Variables

#### Backend
```bash
cd backend
copy .env.example .env
```

Edit `backend\.env` with your credentials:
```env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/tododb
JWT_SECRET_KEY=your-secret-key-change-in-production
OPENAI_API_KEY=sk-your-openai-api-key-here
OPENAI_MODEL=gpt-4o-mini
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

#### Frontend
```bash
cd frontend
copy .env.local.example .env.local
```

Edit `frontend\.env.local`:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```

### 3. Setup Database
```bash
# Create PostgreSQL database
psql -U postgres
CREATE DATABASE tododb;
\q
```

### 4. Install Dependencies

#### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

#### Frontend
```bash
cd frontend
npm install
```

### 5. Run the Application

#### Option A: Using Start Script (Windows)
```bash
# From project root
start.bat
```

#### Option B: Manual Start
```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 6. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📖 Documentation

- **[SETUP_GUIDE.md](./SETUP_GUIDE.md)** - Detailed setup instructions
- **[VERIFICATION_CHECKLIST.md](./VERIFICATION_CHECKLIST.md)** - Testing checklist
- **[API Docs](http://localhost:8000/docs)** - Interactive API documentation

## 🏗️ Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Frontend  │◄───────►│   Backend    │◄───────►│  Database   │
│  Next.js 16 │  HTTP   │  FastAPI     │  SQL    │ PostgreSQL  │
│  React 19   │  REST   │  Python      │         │  asyncpg    │
└─────────────┘         └──────────────┘         └─────────────┘
                              │
                              ▼
                        ┌──────────────┐
                        │  OpenAI API  │
                        │  Agents SDK  │
                        └──────────────┘
```

### Project Structure
```
Hakhaton-2-TodoApp-Phase-III/
├── backend/
│   ├── app/
│   │   ├── auth/          # Authentication (JWT)
│   │   ├── routes/        # API endpoints
│   │   ├── services/      # Business logic
│   │   ├── config.py      # Configuration
│   │   ├── db.py          # Database setup
│   │   ├── main.py        # FastAPI app
│   │   └── models.py      # SQLModel models
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/               # Next.js app router
│   ├── hooks/             # React hooks
│   ├── src/
│   │   ├── components/    # React components
│   │   └── services/      # API services
│   ├── package.json
│   └── .env.local.example
├── SETUP_GUIDE.md
├── VERIFICATION_CHECKLIST.md
└── start.bat
```

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login user |
| GET | `/api/auth/me` | Get current user |

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | List all tasks |
| POST | `/api/tasks` | Create task |
| GET | `/api/tasks/{id}` | Get specific task |
| PATCH | `/api/tasks/{id}` | Update task |
| DELETE | `/api/tasks/{id}` | Delete task |

### Chatbot
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/{user_id}/chat` | Send message to AI |
| GET | `/api/conversations/{user_id}` | Get conversations |
| DELETE | `/api/conversations/{id}` | Delete conversation |

## 🧪 Testing

### Test Authentication
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

### Test Chatbot
```bash
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"content": "Add a task to buy groceries"}'
```

## 🚀 Deployment

### Frontend (Vercel)
1. Install Vercel CLI: `npm install -g vercel`
2. Set environment variables in Vercel dashboard
3. Deploy: `vercel`

### Backend (Railway/Render)
1. Create new project
2. Connect GitHub repository
3. Set environment variables
4. Deploy automatically on push

### Environment Variables for Production

**Backend:**
```env
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
JWT_SECRET_KEY=<strong-random-key>
OPENAI_API_KEY=sk-production-key
DEBUG=False
ALLOWED_ORIGINS=https://your-app.vercel.app
```

**Frontend:**
```env
NEXT_PUBLIC_API_BASE_URL=https://your-backend-api.com/api
```

## 🔒 Security

- **Password Hashing**: SHA-256 + bcrypt for extra security
- **JWT Authentication**: Secure token-based auth (7-day expiry)
- **CORS Protection**: Configured allowed origins
- **SQL Injection Protection**: Using SQLModel ORM
- **Environment Variables**: Sensitive data in `.env` files

## 🐛 Troubleshooting

### Chatbot not responding
- Verify `OPENAI_API_KEY` is set correctly
- Check API key has available credits
- Review backend logs for errors

### Database connection errors
- Ensure PostgreSQL is running
- Verify `DATABASE_URL` credentials
- Check database exists

### CORS errors
- Update `ALLOWED_ORIGINS` in backend `.env`
- Include both http and https URLs

### Authentication issues
- Clear browser localStorage
- Re-login to get fresh token
- Check `JWT_SECRET_KEY` is set

## 📝 License

This project is part of Hakhaton Phase III.

## 👥 Credits

**Developer**: [Your Name]
**Phase**: III - AI-Powered Todo Chatbot
**Technologies**: FastAPI, Next.js, OpenAI Agents SDK, PostgreSQL

---

**For detailed setup instructions, see [SETUP_GUIDE.md](./SETUP_GUIDE.md)**

**For testing checklist, see [VERIFICATION_CHECKLIST.md](./VERIFICATION_CHECKLIST.md)**
