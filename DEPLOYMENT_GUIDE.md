# Deployment Guide - CodeAura Backend

## 🚀 Deployment Options

Choose one of these platforms to deploy your Flask backend:

1. **Render** (Recommended - Free tier available)
2. **Railway** (Easy to use)
3. **Heroku** (Alternative)
4. **AWS** (For production scale)

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All tests pass locally
- [ ] `.env.example` is up to date
- [ ] Database migrations are ready
- [ ] SECRET_KEY is changed
- [ ] JWT keys are configured
- [ ] Static files are collected
- [ ] Git repository is initialized
- [ ] `.gitignore` is set properly

---

## 🔧 Option 1: Deploy on Render (RECOMMENDED)

Render is beginner-friendly and has a free tier with PostgreSQL.

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Authorize Render to access your repositories

### Step 2: Create `render.yaml`
Create this file in your project root:

```yaml
services:
  - type: web
    name: codeaura-backend
    env: python
    plan: free
    buildCommand: |
      pip install -r requirements.txt
    startCommand: gunicorn app:create_app()
    envVars:
      - key: FLASK_ENV
        value: production
      - key: PYTHON_VERSION
        value: 3.11
      - key: SECRET_KEY
        generateValue: true
      - key: JWT_SECRET_KEY
        generateValue: true
      - key: DATABASE_URL
        value: ${DATABASE_URL}
```

### Step 3: Create Procfile
```
web: gunicorn app:create_app()
```

### Step 4: Update requirements.txt
Add gunicorn to your `requirements.txt`:
```
gunicorn==21.2.0
psycopg2-binary==2.9.9  # For PostgreSQL
```

### Step 5: Create `.env` on Render Dashboard
1. Go to your Render service
2. Click "Environment"
3. Add these variables:

```
FLASK_ENV=production
SECRET_KEY=your-very-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=postgresql://user:password@host/dbname
RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret
```

### Step 6: Connect Database
1. Click "PostgreSQL" in Render dashboard
2. Create new database
3. Copy connection string to `DATABASE_URL`

### Step 7: Deploy
1. Push code to GitHub
2. Connect repository in Render
3. Click "Deploy"
4. Monitor build logs

**Your app will be live at:** `https://codeaura-backend.onrender.com`

---

## 📦 Option 2: Deploy on Railway

### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

### Step 2: Login to Railway
```bash
railway login
```

### Step 3: Create `railway.json`
```json
{
  "builder": "dockerfile",
  "buildCommand": "pip install -r requirements.txt",
  "start": "gunicorn app:create_app()"
}
```

### Step 4: Initialize Railway Project
```bash
railway init
```

### Step 5: Add PostgreSQL
```bash
railway add --name postgres
```

### Step 6: Set Environment Variables
```bash
railway variables set FLASK_ENV production
railway variables set SECRET_KEY your-secret-key
railway variables set JWT_SECRET_KEY your-jwt-secret
railway variables set DATABASE_URL postgresql://...
```

### Step 7: Deploy
```bash
railway up
```

### Step 8: View Logs
```bash
railway logs
```

---

## 🐳 Option 3: Docker Deployment

### Step 1: Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create uploads directory
RUN mkdir -p uploads

# Expose port
EXPOSE 5000

# Set environment
ENV FLASK_ENV=production

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:create_app()"]
```

### Step 2: Create .dockerignore
```
__pycache__
*.pyc
.env
.git
venv/
uploads/
*.db
```

### Step 3: Build Docker Image
```bash
docker build -t codeaura-backend:latest .
```

### Step 4: Run Container Locally
```bash
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e DATABASE_URL=postgresql://user:pass@db:5432/codeaura \
  codeaura-backend:latest
```

---

## 🛠️ Setup Production Database

### Option A: PostgreSQL on Render
1. Go to Render Dashboard
2. Click "New +"
3. Select "PostgreSQL"
4. Copy connection string
5. Add to your backend `.env`

### Option B: MySQL on AWS RDS
```bash
# Install MySQL client
pip install PyMySQL

# Update DATABASE_URL
DATABASE_URL=mysql+pymysql://user:password@rds-endpoint:3306/codeaura
```

### Option C: Supabase (PostgreSQL)
1. Go to [supabase.com](https://supabase.com)
2. Create new project
3. Copy connection string
4. Add to `.env`

---

## 🔐 Production Environment Variables

Required for production:

```env
# Flask
FLASK_ENV=production
DEBUG=False
SECRET_KEY=generate-strong-random-key-32-chars-min

# Database
DATABASE_URL=postgresql://user:password@host:5432/codeaura

# JWT
JWT_SECRET_KEY=generate-another-strong-key

# Razorpay (Optional)
RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret

# Firebase (Optional)
FIREBASE_API_KEY=your_key
FIREBASE_PROJECT_ID=your_project
FIREBASE_AUTH_DOMAIN=your_domain

# WhatsApp (Optional)
WHATSAPP_BUSINESS_ACCOUNT_ID=your_account
WHATSAPP_ACCESS_TOKEN=your_token

# Server
SERVER_HOST=0.0.0.0
SERVER_PORT=5000
```

---

## 📊 Production Checklist

Before going live:

### Security
- [ ] Change SECRET_KEY to strong random value
- [ ] Change JWT_SECRET_KEY
- [ ] Enable HTTPS
- [ ] Setup firewall rules
- [ ] Configure CORS properly
- [ ] Add rate limiting

### Performance
- [ ] Enable caching
- [ ] Setup CDN for static files
- [ ] Configure database connection pooling
- [ ] Setup monitoring/logging
- [ ] Configure backups

### Monitoring
- [ ] Setup error tracking (Sentry)
- [ ] Setup logging (CloudWatch, Datadog)
- [ ] Monitor uptime
- [ ] Monitor database performance
- [ ] Alert on errors

### Database
- [ ] Backup regularly
- [ ] Test recovery process
- [ ] Monitor database size
- [ ] Optimize slow queries
- [ ] Setup read replicas if needed

---

## 🚀 Quick Deploy Command (Render)

If you have Render CLI installed:

```bash
# Login to Render
render login

# Deploy
render deploy --project-name codeaura-backend
```

---

## 📝 Environment Variable Generator

Generate secure keys:

```python
import secrets
import string

# Generate SECRET_KEY
secret_key = secrets.token_urlsafe(32)
print(f"SECRET_KEY={secret_key}")

# Generate JWT_SECRET_KEY
jwt_key = secrets.token_urlsafe(32)
print(f"JWT_SECRET_KEY={jwt_key}")
```

---

## 🔍 Test Deployment

After deployment:

```bash
# Test health endpoint
curl https://your-app.onrender.com/api/health

# Test API
curl https://your-app.onrender.com/api

# Login (should fail without valid credentials)
curl -X POST https://your-app.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test"}'
```

---

## 🐛 Troubleshooting

### Build Failed
- Check `requirements.txt` compatibility
- Verify Python version
- Check for syntax errors
- Review build logs

### Database Connection Error
- Verify DATABASE_URL is correct
- Check database is running
- Test connection locally first
- Check firewall/IP whitelist

### 502 Bad Gateway
- Check app logs
- Verify app is listening on correct port
- Check for startup errors
- Restart application

### Static Files Not Loading
- Run `python app.py` to verify locally
- Check static folder path
- Clear cache
- Check file permissions

---

## 📊 Monitoring & Logging

### Setup Sentry (Error Tracking)
```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

### Setup CloudWatch Logging
```python
import logging
import watchtower

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(watchtower.CloudWatchLogHandler())
```

---

## 💾 Database Backups

### Automated Backups on Render
1. Go to PostgreSQL service
2. Click "Backups"
3. Enable automated backups
4. Set retention period

### Manual Backup
```bash
# Export database
pg_dump postgresql://user:pass@host/db > backup.sql

# Import database
psql postgresql://user:pass@host/db < backup.sql
```

---

## 🔄 CI/CD Setup (GitHub Actions)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pytest
      - name: Deploy to Render
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: |
          curl -X POST https://api.render.com/v1/services/${{ secrets.RENDER_SERVICE_ID }}/deploys \
            -H "Authorization: Bearer $RENDER_API_KEY"
```

---

## 🎯 Next Steps After Deployment

1. ✅ Test all API endpoints
2. ✅ Test admin panel
3. ✅ Setup error monitoring
4. ✅ Setup logging
5. ✅ Configure backups
6. ✅ Update Flutter app API URL
7. ✅ Setup custom domain
8. ✅ Enable HTTPS
9. ✅ Monitor performance
10. ✅ Celebrate! 🎉

---

## 📞 Support

For deployment issues:
- Check platform documentation
- Review build/deployment logs
- Test locally first
- Check environment variables
- Verify database connectivity

---

## 🎓 Learning Resources

- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Docker Docs](https://docs.docker.com)
- [Flask Deployment](https://flask.palletsprojects.com/deployment/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

---

**Your CodeAura backend is ready to deploy!** 🚀
