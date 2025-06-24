# 🚀 Quick Deployment Guide

## 🏃‍♂️ **SUPER FAST DEPLOYMENT** (5 minutes total)

### Step 1: GitHub Upload (2 minutes)

1. **Go to GitHub.com** and create a new repository named `nirabhi-ai-moderator`
2. **Copy the git remote URL** (like `https://github.com/yourusername/nirabhi-ai-moderator.git`)
3. **Run these commands** in your project folder:

```bash
git remote add origin YOUR_GITHUB_URL_HERE
git branch -M main
git push -u origin main
```

### Step 2: Deploy Backend on Railway (2 minutes)

1. **Go to [Railway.app](https://railway.app)** 
2. **Sign up with GitHub** (1 click)
3. **Click "New Project"** → **"Deploy from GitHub repo"**
4. **Select your `nirabhi-ai-moderator` repository**
5. **Railway will auto-deploy!** ✨

Your backend will be live at: `https://your-app-name.railway.app`

### Step 3: Deploy Frontend on Vercel (1 minute)

1. **Go to [Vercel.com](https://vercel.com)**
2. **Sign up with GitHub** (1 click)
3. **Click "New Project"** → **Import your GitHub repo**
4. **Set these settings:**
   - Framework: `Create React App`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `build`
5. **Click Deploy!** ✨

Your frontend will be live at: `https://your-app-name.vercel.app`

## 🎯 **Alternative: All-in-One Deployment**

### Option A: Render.com (Easiest)
1. Go to [Render.com](https://render.com)
2. Connect GitHub
3. Import repository
4. Select "Web Service"
5. Deploy automatically!

### Option B: Netlify (Frontend Only)
1. Go to [Netlify.com](https://netlify.com)
2. Drag & drop your `frontend/build` folder
3. Live in 30 seconds!

## 🔗 **Update Frontend to Use Live Backend**

After backend is deployed, update `frontend/src/components/ContentAnalyzer.tsx`:

Change line 77:
```typescript
const response = await axios.post('/analyze', {
```

To:
```typescript
const response = await axios.post('https://YOUR-RAILWAY-APP.railway.app/analyze', {
```

Then redeploy frontend!

## 🎉 **You're Live!**

Your AI Content Moderator is now running on the internet! 

- **Frontend**: Your Vercel/Netlify URL
- **Backend**: Your Railway/Render URL  
- **GitHub**: Your repository URL

**Perfect for hackathon submission!** 🏆

## 🆘 **Need Help?**

If something breaks:
1. Check the deployment logs
2. Make sure all environment variables are set
3. Verify the backend URL in frontend code
4. Railway/Vercel have great support docs

**Total time from code to live: 5-10 minutes!** ⚡
