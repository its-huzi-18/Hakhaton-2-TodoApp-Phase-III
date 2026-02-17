# Vercel Deployment Guide - Backend

## ⚠️ CRITICAL: Root Directory Setting

When deploying the backend to Vercel, you **MUST** set the Root Directory in Vercel dashboard settings.

## Step-by-Step Deployment

### 1. Create New Project in Vercel
1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import your GitHub repository: `Hakhaton-2-TodoApp-Phase-III`

### 2. Configure Project Settings (BEFORE clicking Deploy)

Click "Configure" or go to Project Settings → General:

#### **Root Directory**
- **Click "Edit"** on Root Directory
- **Enter:** `backend`
- This tells Vercel to only deploy the backend folder

#### **Build Command**
- **Framework Preset:** Python
- **Build Command:** `pip install -r requirements.txt`

#### **Output Directory**
- Leave empty (default)

### 3. Environment Variables

Add these in Vercel Dashboard → Settings → Environment Variables:

```
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/dbname
JWT_SECRET_KEY=your-super-secret-key-change-this
OPENAI_API_KEY=sk-your-openai-key
ALLOWED_ORIGINS=https://your-frontend.vercel.app
DEBUG=false
```

### 4. Deploy

Click "Deploy"

## Troubleshooting

### "250 MB size error"
This happens when:
1. **Root Directory is NOT set** - Vercel deploys entire repo
2. **node_modules or venv in git** - Make sure they're in .gitignore

**Fix:**
1. Go to Vercel Dashboard → Your Backend Project → Settings → General
2. Find "Root Directory"
3. Set it to: `backend`
4. Redeploy

### "Failed to run uv sync" or "Failed to run uv lock" error
This happens when Vercel detects `pyproject.toml`, `package.json`, or `uv.lock` and tries to use `uv` package manager instead of `pip`.

**Fix (Already Applied):**
- ✅ `pyproject.toml` has been removed from backend
- ✅ `package.json` has been removed from backend
- ✅ Version folders (0.27.0, etc.) have been removed
- ✅ Only `requirements.txt` remains
- ✅ Vercel will now use `pip install -r requirements.txt`
- ✅ Make sure Root Directory is set to `backend`

If you still see this error:
1. Delete your Vercel project
2. Create a new one
3. Set Root Directory to `backend` BEFORE first deploy
4. Deploy

### Still getting size error?

1. Delete the Vercel project
2. Create a new one
3. **IMMEDIATELY** set Root Directory to `backend` BEFORE first deploy
4. Then deploy

## File Structure

Vercel will deploy this structure:
```
backend/
├── api/
│   └── index.py          # Entry point for Vercel
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app
│   ├── config.py
│   ├── db.py
│   ├── models.py
│   ├── auth/
│   ├── routes/
│   └── services/
├── requirements.txt      # Dependencies
├── vercel.json          # Vercel config
└── .vercelignore        # Files to exclude
```

## Important Notes

- `__pycache__/` is ignored
- `venv/` is ignored
- `node_modules/` is ignored
- Test files are excluded via `.vercelignore`
- Version folders (0.27.0, etc.) are ignored
