# Fix: Invalid User ID Format Error

## Problem
You're seeing this error:
```
HTTP error! status: 400 - Invalid user ID format: 32jxwkewkzf. Expected a valid UUID.
```

This happens because you have an **old user session** stored in your browser's localStorage from before the UUID fix was implemented.

## Solution (Quick Fix)

### Option 1: Clear LocalStorage (Recommended)

1. Open your browser's Developer Tools (F12)
2. Go to the **Application** tab (Chrome) or **Storage** tab (Firefox)
3. In the left sidebar, expand **Local Storage**
4. Click on `http://localhost:3000` (or your frontend URL)
5. Click **Clear All** or delete the `user` and `token` keys
6. Refresh the page
7. Login again

### Option 2: Use Browser Console

1. Open your browser (while on your app)
2. Press **F12** to open Developer Tools
3. Go to the **Console** tab
4. Paste this command and press Enter:
   ```javascript
   localStorage.clear(); window.location.reload();
   ```
5. Login again

### Option 3: Manual Console Command

1. Open browser console (F12)
2. Run:
   ```javascript
   localStorage.removeItem('user');
   localStorage.removeItem('token');
   window.location.reload();
   ```
3. Login again

## Why This Happened

Your old user session had a short ID like `32jxwkewkzf` instead of a proper UUID format like:
```
550e8400-e29b-41d4-a716-446655440000
```

The backend now requires proper UUID format for security and consistency.

## After Fixing

Once you've cleared localStorage and re-logged in:

1. Your new user will have a proper UUID
2. The chatbot will work correctly
3. All task operations will work

## Verify It's Fixed

After logging in again:
1. Open browser console (F12)
2. Run: `console.log(JSON.parse(localStorage.getItem('user')))`
3. Check that the `id` looks like: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

Example of valid UUID:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "test@example.com"
}
```

## Prevention

This won't happen again because:
- The chat page now validates UUID format automatically
- Invalid sessions will trigger auto-logout
- You'll be prompted to re-login with a proper UUID
