# 🚀 Deploy CodeAura Backend to Render - Step by Step

**Estimated Time:** 15-20 minutes  
**Cost:** FREE (Render free tier)  
**Your Live URL:** `https://codeaura-backend.onrender.com`

---

## ✅ Prerequisites (Already Done)

- ✅ Code pushed to GitHub: `https://github.com/muhibmansuri/codeaura`
- ✅ Dockerfile ready
- ✅ render.yaml configured
- ✅ requirements.txt with dependencies
- ✅ .env.example with all variables

---

## 📋 Step 1: Create Render Account (2 minutes)

1. Go to **[render.com](https://render.com)**
2. Click **"Sign Up"**
3. Choose **"Sign up with GitHub"**
4. Authorize Render to access your GitHub
5. Verify email (check inbox)
6. Done! ✅

---

## 🔗 Step 2: Connect GitHub Repository (2 minutes)

1. After login, go to Render Dashboard
2. Click **"+ New +"** (top right)
3. Select **"Web Service"**
4. Under "Connect a repository" → Click **"Connect"**
5. Find **"codeaura"** repository
6. Click **"Connect"**
7. You'll see form to fill in → Next step

---

## ⚙️ Step 3: Configure Web Service (3 minutes)

Fill in these details in the form:

| Field | Value |
|-------|-------|
| **Name** | `codeaura-backend` |
| **Environment** | `Python 3` |
| **Region** | `Singapore` or `US` (your choice) |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:create_app()` |
| **Instance Type** | `Free` |

Then click **"Create Web Service"** → Building starts...

---

## 🗄️ Step 4: Create PostgreSQL Database (5 minutes)

While the web service is building:

1. Click **"+ New +"** again
2. Select **"PostgreSQL"**
3. Fill in:

| Field | Value |
|-------|-------|
| **Name** | `codeaura-db` |
| **Database** | `codeaura` |
| **User** | `codeaura_user` |
| **Region** | `Singapore` (same as web service) |
| **Instance Type** | `Free` |

4. Click **"Create Database"**
5. Database will start → Take note of connection info

---

## 🔐 Step 5: Add Environment Variables (3 minutes)

Once Web Service is building (status shows "Building"):

1. Go to your **Web Service** (codeaura-backend)
2. Click **"Environment"** tab (left sidebar)
3. Click **"Add Environment Variable"** for each:

### Required Variables:

```
FLASK_ENV = production
DEBUG = False
DATABASE_URL = postgresql://codeaura_user:<PASSWORD>@<HOST>:5432/codeaura
SECRET_KEY = <generate-below>
JWT_SECRET_KEY = <generate-below>
```

### How to get DATABASE_URL:
1. Go to your PostgreSQL database page
2. Look for "Internal Database URL" or "Connection String"
3. Copy and paste it exactly

### How to generate SECRET_KEY and JWT_SECRET_KEY:

Run this in PowerShell:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Run it twice to get 2 different keys.

---

## 📍 Step 6: Connect Database to Web Service (2 minutes)

1. On your **Web Service** page
2. Go to **"Environment"** tab
3. Add this variable:

```
DATABASE_URL = postgresql://codeaura_user:<PASSWORD>@<HOST>:5432/codeaura
```

4. Save/Deploy

---

## 🚀 Step 7: Deploy (Automatic)

Once you:
- ✅ Configured Web Service
- ✅ Created PostgreSQL database
- ✅ Added all environment variables

**Render automatically deploys!**

Watch the build logs in real-time on the dashboard.

**Status should show:**
- `Building...` → `Deploying...` → `Live ✓`

Takes about **3-5 minutes**

---

## ✅ Step 8: Verify Deployment (2 minutes)

Once status shows **"Live"**, test your backend:

### Test 1: Health Check
```powershell
curl https://codeaura-backend.onrender.com/api/health
```

Expected response:
```json
{"status": "healthy", "database": "connected"}
```

### Test 2: Get Courses (No Auth Required)
```powershell
curl https://codeaura-backend.onrender.com/api/courses
```

Expected response:
```json
{"courses": [], "total": 0}
```

### Test 3: Login (Admin Panel)
```powershell
curl -X POST https://codeaura-backend.onrender.com/admin/login `
  -H "Content-Type: application/json" `
  -d '{"username": "admin", "password": "admin123"}'
```

If you see successful responses → **Deployment successful!** 🎉

---

## 🌐 Your Live URLs

After successful deployment:

| Service | URL |
|---------|-----|
| **API Base** | `https://codeaura-backend.onrender.com/api` |
| **Admin Panel** | `https://codeaura-backend.onrender.com/admin` |
| **Health Check** | `https://codeaura-backend.onrender.com/api/health` |

---

## 📊 Monitor Your Deployment

1. **View Logs**
   - Dashboard → Web Service → **"Logs"** tab
   - Real-time logs appear here
   - Check for errors or issues

2. **Metrics**
   - Dashboard → Web Service → **"Metrics"** tab
   - CPU, Memory, Network usage

3. **Redeploy (if needed)**
   - Dashboard → Web Service → **"Manual Deploy"** button
   - Or push code to GitHub (auto-redeploys)

---

## 🔄 Auto Redeploy on GitHub Push

Render automatically redeploys when you push to GitHub!

```powershell
# After making changes locally:
git add .
git commit -m "Description of changes"
git push origin main

# Render automatically triggers deployment
```

---

## 🐛 Troubleshooting

### ❌ "502 Bad Gateway" Error?

**Cause:** App crashed or port issue

**Solution:**
1. Check Logs tab for error messages
2. Verify all environment variables are set
3. Check DATABASE_URL format
4. Restart the service (Manual Deploy)

### ❌ "Database connection refused"?

**Cause:** Wrong DATABASE_URL or database not running

**Solution:**
1. Copy DATABASE_URL from PostgreSQL page again
2. Verify credentials are correct
3. Check database status (should be "Available")
4. Restart both web service and database

### ❌ "ModuleNotFoundError"?

**Cause:** Missing dependency in requirements.txt

**Solution:**
1. Add missing package to `backend/requirements.txt`
2. Push to GitHub
3. Render auto-redeploys

### ❌ Build failing?

**Cause:** Python version or syntax error

**Solution:**
1. Check build logs for specific error
2. Test locally first: `python app.py`
3. Fix issue and push to GitHub
4. Render retries automatically

---

## 🎯 Quick Checklist

Before deploying, ensure:

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] GitHub connected to Render
- [ ] Web Service created with correct settings
- [ ] PostgreSQL database created
- [ ] All environment variables set
- [ ] Build successful (status shows "Live")
- [ ] Health endpoint responding
- [ ] Database connected (no connection errors)

---

## 📱 Update Flutter App (After Deployment)

Once backend is live, update your Flutter app:

```dart
// lib/config/api_config.dart

// OLD (local development)
// const String API_URL = 'http://localhost:5000';

// NEW (production on Render)
const String API_URL = 'https://codeaura-backend.onrender.com';
```

---

## 🎓 Learning Resources

- [Render Docs](https://render.com/docs)
- [Python Web Services on Render](https://render.com/docs/deploy-flask)
- [Environment Variables](https://render.com/docs/environment-variables)
- [PostgreSQL on Render](https://render.com/docs/databases)

---

## ✨ You're All Set!

Your CodeAura backend is ready for production deployment!

**Next Steps:**
1. Create Render account at render.com
2. Follow steps 2-8 above
3. Verify deployment with health check
4. Update Flutter app with live URL
5. Start building mobile app!

**Questions?** Check troubleshooting section or Render docs.

**Let's go! 🚀**
