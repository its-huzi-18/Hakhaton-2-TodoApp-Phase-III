# 🚨 CRITICAL FIX - Do This NOW!

## Your Problem
You keep getting:
```
Invalid user ID format: wh6feht90e
```

This is because:
1. Your localStorage has old user with short ID
2. Frontend was calling wrong backend URLs

## ✅ What I Just Fixed

### Backend URLs
- **Before:** `/api/auth/login` ❌
- **After:** `/auth/login` ✅

### API Service
- **Before:** `http://localhost:8000/api` ❌  
- **After:** `http://localhost:8000` ✅

## 🛑 DO THIS NOW (30 seconds):

### Step 1: Clear LocalStorage
Open browser console (F12) and run:
```javascript
localStorage.clear();
console.log('✅ Cleared!');
```

### Step 2: Refresh Page
Press F5 or run:
```javascript
window.location.reload();
```

### Step 3: Register New Account
1. Go to: http://localhost:3000/auth/signup
2. Register with email/password
3. You'll get a NEW user with proper UUID

### Step 4: Test Chat
1. Go to: http://localhost:3000/chat
2. Send a message
3. Should work now! ✅

## Why This Happened

1. Frontend was calling `/api/auth/login` but backend is at `/auth/login`
2. Some proxy/middleware was creating users with short IDs
3. Your localStorage kept the invalid user

## Files I Fixed

1. **frontend/hooks/auth.ts**
   - Changed login URL to `${API_BASE_URL}/auth/login`
   - Changed register URL to `${API_BASE_URL}/auth/register`
   - Fixed token key from `data.token` to `data.access_token`

2. **frontend/src/services/api.js**
   - Changed base URL from `http://localhost:8000/api` to `http://localhost:8000`
   - Updated endpoints to include `/api` prefix correctly

## Verification

After registering new account, check console:
```javascript
const user = JSON.parse(localStorage.getItem('user'));
console.log(user.id);
// Should show: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

## If It Still Doesn't Work

1. **Kill all servers**
2. **Clear browser cache** (Ctrl+Shift+Delete)
3. **Restart frontend:** `npm run dev`
4. **Restart backend:** `python -m uvicorn app.main:app --reload`
5. **Register fresh account**

---

**STATUS:** Fixed backend URLs + API paths  
**ACTION REQUIRED:** Clear localStorage + Register new account
