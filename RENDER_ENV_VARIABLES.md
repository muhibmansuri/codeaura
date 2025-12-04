# 🔐 Deployment Credentials & Environment Variables

**Generated:** December 4, 2025  
**For:** CodeAura Backend on Render  

---

## 🔑 Your Generated Secret Keys

Copy these into Render Environment Variables:

### SECRET_KEY
```
RktJhyXNUeCqnph1GmrheMDwgR4bddTY17K-NQpID_I
```

### JWT_SECRET_KEY
```
uOdN_NgyjkXotgjBu07_Cmr-nX2jsms8qdPFuj1r5bI
```

---

## 📋 Complete Environment Variables for Render

Add these in Render Dashboard → Environment tab:

```
FLASK_ENV=production
DEBUG=False
SECRET_KEY=RktJhyXNUeCqnph1GmrheMDwgR4bddTY17K-NQpID_I
JWT_SECRET_KEY=uOdN_NgyjkXotgjBu07_Cmr-nX2jsms8qdPFuj1r5bI
DATABASE_URL=postgresql://codeaura_user:PASSWORD@HOST:5432/codeaura
```

**Note:** Replace `PASSWORD` and `HOST` with your PostgreSQL database credentials from Render.

---

## 🗄️ PostgreSQL Database Info (After Creating)

When you create PostgreSQL database on Render, you'll get:

```
Username: codeaura_user
Database: codeaura
Host: [will-appear-in-render-dashboard]
Port: 5432
Password: [auto-generated-by-render]
```

**Full Connection String Format:**
```
postgresql://codeaura_user:PASSWORD@HOST:5432/codeaura
```

---

## ✅ Render Deployment Checklist

- [ ] Render account created at render.com
- [ ] GitHub repository connected
- [ ] Web Service created (codeaura-backend)
- [ ] PostgreSQL database created (codeaura-db)
- [ ] Root Directory set to: `backend`
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `gunicorn app:create_app()`
- [ ] All environment variables added
- [ ] Web Service status: "Live"
- [ ] Health check endpoint responds: `/api/health`

---

## 🚀 Quick Steps Summary

1. **Create Render Account** → render.com/sign-up
2. **Connect GitHub** → Authorize codeaura repo
3. **Create Web Service**
   - Name: `codeaura-backend`
   - Root Dir: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:create_app()`
4. **Create PostgreSQL** → Free tier
5. **Add Environment Variables** → Copy from above
6. **Deploy** → Automatic, takes 3-5 minutes
7. **Test** → `curl https://codeaura-backend.onrender.com/api/health`

---

## 📱 Update Flutter App

Once deployed, use this API URL:

```dart
const String API_URL = 'https://codeaura-backend.onrender.com';
```

---

## 🔗 References

- Full Guide: See `RENDER_DEPLOYMENT_STEPS.md`
- General Deployment: See `DEPLOYMENT_GUIDE.md`
- Render Docs: https://render.com/docs

---

**Status:** Ready for deployment  
**Next Action:** Go to https://render.com and follow RENDER_DEPLOYMENT_STEPS.md
