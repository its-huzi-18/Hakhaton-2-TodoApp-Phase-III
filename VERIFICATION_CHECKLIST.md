# ✅ Pre-Launch Verification Checklist

## Before Running Locally

### 1. Environment Setup

#### Backend (.env file)
- [ ] Copy `backend/.env.example` to `backend/.env`
- [ ] Set `DATABASE_URL` with your PostgreSQL credentials
- [ ] Set `JWT_SECRET_KEY` (use a strong random string)
- [ ] Set `OPENAI_API_KEY` with your actual API key
- [ ] Verify `ALLOWED_ORIGINS` includes `http://localhost:3000`

#### Frontend (.env.local file)
- [ ] Copy `frontend/.env.local.example` to `frontend/.env.local`
- [ ] Verify `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api`

### 2. Database Setup
- [ ] PostgreSQL is installed and running
- [ ] Database `tododb` exists (or create it)
- [ ] Database credentials in `DATABASE_URL` are correct

### 3. Dependencies Installed

#### Backend
```bash
cd backend
pip install -r requirements.txt
```
- [ ] All Python packages installed successfully
- [ ] No import errors when running `python -c "from app.main import app"`

#### Frontend
```bash
cd frontend
npm install
```
- [ ] All Node packages installed successfully
- [ ] No errors when running `npm run build`

## Running Locally

### Start Backend
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- [ ] Server starts without errors
- [ ] Logs show "Uvicorn running on http://0.0.0.0:8000"

### Start Frontend
```bash
cd frontend
npm run dev
```
- [ ] Server starts without errors
- [ ] Logs show "Ready in Xms"
- [ ] No compilation errors

### Verify Endpoints

#### Backend Health Check
```bash
curl http://localhost:8000/health
```
- [ ] Returns: `{"status": "healthy"}`

#### API Documentation
- [ ] Visit http://localhost:8000/docs
- [ ] Swagger UI loads correctly
- [ ] All endpoints are listed

#### Frontend
- [ ] Visit http://localhost:3000
- [ ] Homepage loads correctly
- [ ] No console errors in browser DevTools

## Functional Testing

### 1. Authentication Flow

#### Register New User
- [ ] Navigate to http://localhost:3000/auth/signup
- [ ] Enter email and password (min 8 chars)
- [ ] Click "Sign up"
- [ ] Redirected to dashboard
- [ ] User data stored in localStorage

#### Login
- [ ] Navigate to http://localhost:3000/auth/login
- [ ] Enter credentials
- [ ] Click "Sign in"
- [ ] Redirected to dashboard
- [ ] Token stored in localStorage

### 2. Task Management

#### Create Task
- [ ] On dashboard, enter task title
- [ ] Optionally add description
- [ ] Click "Add Task"
- [ ] Task appears in the list
- [ ] Success notification shown

#### View Tasks
- [ ] Tasks display in the list
- [ ] Title and description visible
- [ ] Created date shown
- [ ] Stats cards update (Total, Completed, Pending)

#### Complete Task
- [ ] Click checkbox on a task
- [ ] Task marked as completed (green styling)
- [ ] "Completed" badge appears
- [ ] Stats update

#### Delete Task
- [ ] Click delete button on a task
- [ ] Task removed from list
- [ ] Stats update

### 3. AI Chatbot

#### Access Chat
- [ ] Navigate to http://localhost:3000/chat
- [ ] Chat interface loads
- [ ] Welcome message from AI visible

#### Test AI Commands

**Add Task via Chat:**
- [ ] Type: "Add a task to buy groceries"
- [ ] AI responds with confirmation
- [ ] Task appears in database
- [ ] Tool call executed successfully

**List Tasks via Chat:**
- [ ] Type: "Show my tasks"
- [ ] AI lists your tasks
- [ ] Tasks formatted with emojis

**Complete Task via Chat:**
- [ ] Type: "Complete task buy groceries"
- [ ] AI confirms completion
- [ ] Task marked as completed in DB

**General Conversation:**
- [ ] Type: "Hello" or "What can you do?"
- [ ] AI responds helpfully
- [ ] Lists available capabilities

### 4. Error Handling

#### Invalid Credentials
- [ ] Login with wrong password
- [ ] Error message shown
- [ ] No crash

#### Empty Task Title
- [ ] Try to create task with empty title
- [ ] Validation prevents submission
- [ ] Error message shown

#### Network Error
- [ ] Stop backend server
- [ ] Try to create task
- [ ] Error message shown gracefully

## Production Readiness

### Environment Variables
- [ ] All `.env` files are in `.gitignore`
- [ ] Production values set in deployment platform
- [ ] `DEBUG=False` in production
- [ ] Strong `JWT_SECRET_KEY` generated
- [ ] Production `ALLOWED_ORIGINS` set correctly

### Database
- [ ] Production PostgreSQL configured
- [ ] Connection string uses SSL
- [ ] Database backups enabled
- [ ] Migrations run successfully

### Backend Deployment
- [ ] Deployed to cloud platform (Railway/Render/AWS)
- [ ] Health endpoint accessible
- [ ] CORS configured for frontend domain
- [ ] Logs visible and monitored

### Frontend Deployment (Vercel)
- [ ] Connected to GitHub
- [ ] Environment variables set in Vercel
- [ ] Build succeeds without errors
- [ ] Site accessible via HTTPS
- [ ] API calls reach backend

### Security
- [ ] HTTPS enabled everywhere
- [ ] No sensitive data in client-side code
- [ ] CORS properly configured
- [ ] SQL injection protection (using SQLModel)
- [ ] Password hashing working (bcrypt)

### Performance
- [ ] Database queries use indexes
- [ ] No N+1 query issues
- [ ] Frontend builds are optimized
- [ ] Images/assets optimized

## Final Checks

### Documentation
- [ ] README.md is up to date
- [ ] SETUP_GUIDE.md reviewed
- [ ] API documentation accessible

### Code Quality
- [ ] No console.log in production code
- [ ] No TypeScript errors
- [ ] No Python linting errors
- [ ] Tests pass (if available)

### Monitoring
- [ ] Error tracking configured (optional)
- [ ] Logging enabled
- [ ] Health checks monitored

## Known Issues & Limitations

### Current Limitations
1. Chatbot tool calling requires proper OpenAI API setup
2. Conversation history limited to last 20 messages
3. No file upload support in chat
4. No task categories/tags

### Future Enhancements
- [ ] Task categories/tags
- [ ] Due dates and reminders
- [ ] Task priorities
- [ ] File attachments
- [ ] Collaborative tasks
- [ ] Email notifications

## Support

If you encounter issues:
1. Check the logs (backend and frontend)
2. Verify environment variables
3. Test API endpoints directly using Swagger docs
4. Clear browser cache and localStorage
5. Restart both servers

## Success Criteria

✅ **Ready to Deploy When:**
- All local tests pass
- Environment variables configured
- Database connected and working
- Authentication flow complete
- Task CRUD operations working
- Chatbot responds to commands
- No console errors
- Production environment configured

---

**Last Updated:** 2026-02-17
**Version:** Phase III
