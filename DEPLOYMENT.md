# Deployment Guide

This guide covers deploying the Medical RAG Agent backend to Render and connecting it to your existing Vercel frontend.

## Prerequisites

- GitHub repository with your code (Already pushed)
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
Render will prompt you to set the following environment variables for `medical-rag-backend`:

- `GROQ_API_KEY`: Your Groq API key
- `CLERK_SECRET_KEY`: Your Clerk secret key
- `CLERK_PUBLISHABLE_KEY`: Your Clerk publishable key

Note: `QDRANT_URL` is automatically set to `http://localhost:6333` by the configuration.

### Step 4: Wait for Deployment
- The backend will deploy as a Docker service.
- It includes a local Qdrant instance for vector storage.
- This may take 5-10 minutes.

### Step 5: Get Backend URL
Once deployed, note the backend URL (e.g., `https://medical-rag-backend.onrender.com`).

## Part 2: Connect Frontend (Vercel) to Backend

You have already deployed the frontend to Vercel: `https://medical-rag-agent-cu3q5ve3p-balavardhan-reddys-projects.vercel.app`

Now you need to tell it where the backend is.

### Step 1: Update Vercel Environment Variables
1. Go to your Vercel Project Dashboard.
2. Go to **Settings** → **Environment Variables**.
3. Add or Update `NEXT_PUBLIC_API_URL`:
   - Value: `https://medical-rag-backend.onrender.com` (The URL from Part 1, Step 5)
   - **Important**: Do not add a trailing slash `/`.
4. Ensure Clerk keys are also set in Vercel:
   - `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
   - `CLERK_SECRET_KEY`

### Step 2: Redeploy Frontend
1. Go to **Deployments** tab in Vercel.
2. Click the three dots on the latest deployment → **Redeploy**.
3. This ensures the new environment variables are baked into the app.

## Part 3: CORS Configuration (Optional but Recommended)

Currently, the backend allows all origins (`*`). For better security, you can restrict it to your Vercel domain.

1. Go to your Render Dashboard → `medical-rag-backend` → **Environment**.
2. Add `BACKEND_CORS_ORIGINS`:
   - Value: `["https://medical-rag-agent-cu3q5ve3p-balavardhan-reddys-projects.vercel.app", "http://localhost:3000"]`
   - Note: The value must be a valid JSON string if parsed as a list, or comma-separated if the app handles it.
   - **Simpler approach**: Just set it to your Vercel domain: `https://medical-rag-agent-cu3q5ve3p-balavardhan-reddys-projects.vercel.app` (The app logic might need adjustment to parse a single string vs list, but currently it expects a list in `config.py`. The default is `["*"]`).
   
   *Recommendation*: Leave it as default (`*`) for now to ensure it works, then tighten security later.

## Troubleshooting

### Backend Issues
- **Service won't start**: Check Render logs. Ensure `GROQ_API_KEY` is correct.
- **Upload fails**: Check if the file is too large or if Qdrant is running (check logs for "Starting Qdrant service...").

### Frontend Issues
- **API Connection Error**: Check browser console (F12). If you see "Network Error" or 404, verify `NEXT_PUBLIC_API_URL` in Vercel.
- **CORS Error**: If you see "CORS policy" errors, ensure the backend is running and `BACKEND_CORS_ORIGINS` allows the Vercel domain (or is `*`).
