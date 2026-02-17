# OpenAI Domain Allowlist Configuration

## Required for Production Deployment

Before deploying your chatbot frontend, you must configure OpenAI's domain allowlist for security.

## Step 1: Deploy Frontend to Get URL

Deploy your frontend to get a production URL:

**Vercel:**
```bash
cd frontend
vercel
```
Your URL will be: `https://your-app.vercel.app`

**Other platforms:**
- GitHub Pages: `https://username.github.io/repo-name`
- Custom domain: `https://yourdomain.com`

## Step 2: Add Domain to OpenAI Allowlist

1. Navigate to: https://platform.openai.com/settings/organization/security/domain-allowlist
2. Click **"Add domain"**
3. Enter your frontend URL (without trailing slash):
   - Example: `https://hakhaton-2-todo-app-phase-iii-front.vercel.app`
4. Click **"Save"**

## Step 3: Get Your Domain Key

After adding the domain, OpenAI will provide a **domain key**. Copy this key.

## Step 4: Configure Environment Variables

### Frontend (.env.local or Vercel Environment):

```env
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your-domain-key-from-openai
```

### Set in Vercel Dashboard:
1. Go to your Vercel project settings
2. Navigate to **Environment Variables**
3. Add `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` with your domain key
4. Redeploy your application

## Local Development

For local development (`localhost:3000`), you typically don't need to configure the domain allowlist. The ChatKit works without domain restrictions on localhost.

## Testing

After configuration:
1. Visit your deployed frontend URL
2. The chatbot should load without domain restriction errors
3. If you see a domain error, verify:
   - Domain is added to allowlist
   - Domain key is correctly set in environment variables
   - Frontend is redeployed after setting environment variables

## Troubleshooting

**Error: "Domain not allowed"**
- Verify domain is added to OpenAI allowlist
- Check for trailing slashes in domain URL
- Wait 5-10 minutes for allowlist to propagate

**Error: "Invalid domain key"**
- Verify `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` is set correctly
- Re-copy the key from OpenAI dashboard (no spaces)

## Security Notes

- Never commit domain keys to Git
- Use environment variables for all sensitive data
- Restrict domain allowlist to production URLs only
- Monitor API usage in OpenAI dashboard
