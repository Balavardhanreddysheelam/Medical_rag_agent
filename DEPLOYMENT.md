# Deployment Guide

This guide covers deploying the Medical RAG Agent to Render (backend) and Vercel (frontend).

## Prerequisites

- GitHub repository with your code
- Render account (https://render.com)
- Vercel account (https://vercel.com)
- Groq API key
- Clerk API keys

## Part 1: Deploy Backend to Render

### Step 1: Create Render Account
1. Go to https://render.com and sign up
2. Connect your GitHub account

### Step 2: Deploy Using render.yaml
1. Click "New" → "Blueprint"
2. Connect your GitHub repository: `Medical_rag_agent`
3. Render will automatically detect the `render.yaml` file
4. Click "Apply"

### Step 3: Configure Environment Variables
Render will prompt you to set the following environment variables:

**For medical-rag-backend:**
- `GROQ_API_KEY`: Your Groq API key

**For medical-rag-frontend:**
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`: Your Clerk publishable key
- `CLERK_SECRET_KEY`: Your Clerk secret key

### Step 4: Wait for Deployment
- Backend will deploy as a Docker service
- Qdrant will deploy as a private service
- Frontend will deploy as a Node.js service
- This may take 5-10 minutes

### Step 5: Get Backend URL
Once deployed, note the backend URL (e.g., `https://medical-rag-backend.onrender.com`)

## Part 2: Deploy Frontend to Vercel

### Step 1: Create Vercel Account
1. Go to https://vercel.com and sign up
2. Connect your GitHub account

### Step 2: Import Repository
1. Click "Add New" → "Project"
2. Import your GitHub repository: `Medical_rag_agent`
3. Vercel will detect it's a Next.js project

### Step 3: Configure Root Directory
- Set **Root Directory** to: `frontend`
- Framework Preset: Next.js (auto-detected)
- Build Command: `npm run build` (auto-detected)
- Output Directory: `.next` (auto-detected)

### Step 4: Configure Environment Variables
Add the following environment variables:

```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
CLERK_SECRET_KEY=your_clerk_secret_key
NEXT_PUBLIC_API_URL=https://medical-rag-backend.onrender.com
```

Replace `https://medical-rag-backend.onrender.com` with your actual Render backend URL.

### Step 5: Deploy
1. Click "Deploy"
2. Wait for the build to complete (2-3 minutes)
3. Your frontend will be live at a Vercel URL (e.g., `https://your-app.vercel.app`)

## Part 3: Update Backend CORS

After deploying the frontend, you need to update the backend to allow requests from your Vercel domain.

### Option 1: Update via Render Dashboard
1. Go to your backend service on Render
2. Go to "Environment" tab
3. Add a new environment variable:
   - Key: `BACKEND_CORS_ORIGINS`
   - Value: `https://your-app.vercel.app`
4. Save and redeploy

### Option 2: Update config.py
Update `backend/app/core/config.py`:
```python
BACKEND_CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "https://your-app.vercel.app"
]
```

Then commit and push to trigger a redeploy.

## Part 4: Test the Deployment

1. Visit your Vercel URL
2. Sign in with Clerk
3. Upload a test PDF
4. Ask a question
5. Verify you get a response

## Troubleshooting

### Backend Issues

**Service won't start:**
- Check Render logs for errors
- Verify all environment variables are set
- Ensure Qdrant service is running

**Upload fails:**
- Check backend logs
- Verify spaCy model is installed (should be in Dockerfile)
- Check Qdrant connection

### Frontend Issues

**Build fails:**
- Check Vercel build logs
- Verify `frontend` root directory is set correctly
- Check that all dependencies are in package.json

**API calls fail:**
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check CORS settings on backend
- Verify backend is running

**Clerk authentication fails:**
- Verify Clerk environment variables are correct
- Check Clerk dashboard for domain settings
- Add Vercel domain to Clerk allowed origins

## Cost Considerations

### Render Free Tier
- 750 hours/month of free usage
- Services spin down after 15 minutes of inactivity
- First request after spin-down may be slow (30-60 seconds)

### Vercel Free Tier
- 100 GB bandwidth/month
- Unlimited deployments
- Automatic HTTPS

## Production Recommendations

For production use, consider:

1. **Upgrade Render Plan**: Use a paid plan to avoid spin-down
2. **Add Monitoring**: Set up error tracking (Sentry, LogRocket)
3. **Enable Analytics**: Add Vercel Analytics
4. **Set up CI/CD**: Automatic deployments on push
5. **Add Rate Limiting**: Protect your API endpoints
6. **Database Backups**: Regular Qdrant data backups
7. **Security Audit**: Review HIPAA compliance requirements

## Alternative: Deploy Everything to Render

If you prefer to deploy both frontend and backend to Render:

1. Use the existing `render.yaml` configuration
2. Both services will deploy together
3. No need for Vercel
4. Frontend URL will be: `https://medical-rag-frontend.onrender.com`

## Support

If you encounter issues:
- Check Render logs: Dashboard → Service → Logs
- Check Vercel logs: Dashboard → Project → Deployments → View Logs
- Review this guide's troubleshooting section
