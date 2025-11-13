# LibraNet Deployment Guide

## 🚀 Deploy to Render (Free)

### Prerequisites
✅ GitHub account
✅ Push your code to GitHub repository

---

## Step-by-Step Deployment

### 1️⃣ Prepare Your Repository

Your project is already configured with:
- ✅ `Procfile` - Tells Render how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `requirements.txt` - Updated with production dependencies

**Commit and push these changes:**
```bash
git add .
git commit -m "Add deployment configuration"
git push origin main
```

---

### 2️⃣ Sign Up for Render

1. Go to https://render.com
2. Click **"Get Started for Free"**
3. Sign up with your GitHub account
4. Authorize Render to access your repositories

---

### 3️⃣ Create PostgreSQL Database

1. From Render Dashboard, click **"New +"** → **"PostgreSQL"**
2. Configure database:
   - **Name**: `libranet-db`
   - **Database**: `libranet`
   - **User**: `libranet`
   - **Region**: Choose closest to you
   - **PostgreSQL Version**: 16
   - **Instance Type**: **Free** ✅
3. Click **"Create Database"**
4. Wait ~2 minutes for database to provision
5. **Copy the "Internal Database URL"** - you'll need this!

---

### 4️⃣ Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository `LibraNet`
3. Configure service:

   **Basic Settings:**
   - **Name**: `libranet`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn main:app` (should auto-detect from Procfile)

   **Instance Type:**
   - Select **"Free"** ✅

---

### 5️⃣ Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"** and add these:

```bash
SECRET_KEY=your-super-secret-key-change-this-to-random-string
SQLALCHEMY_DATABASE_URI=<paste-internal-database-url-from-step-3>
FLASK_ENV=production

# Email Configuration (Gmail)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password

# Google OAuth (optional - for Google login)
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret

# GitHub OAuth (optional - for GitHub login)
GITHUB_OAUTH_CLIENT_ID=your-github-client-id
GITHUB_OAUTH_CLIENT_SECRET=your-github-client-secret

# Razorpay (optional - for payments)
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret

# LangChain (optional - for chatbot)
LANGCHAIN_API_KEY=your-langchain-api-key
LANGCHAIN_PROJECT=LibraNet
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

### 6️⃣ Deploy!

1. Click **"Create Web Service"**
2. Render will:
   - Clone your repository
   - Install dependencies
   - Start your application
3. **First deploy takes 5-10 minutes** ⏱️
4. Watch the logs for any errors

---

### 7️⃣ Run Database Migrations

Once deployed, you need to initialize the database:

1. Go to your web service in Render
2. Click **"Shell"** tab
3. Run these commands:
```bash
flask db upgrade
python seed_db.py  # If you have seed data
```

---

### 8️⃣ Access Your App! 🎉

Your app will be available at:
```
https://libranet.onrender.com
```
(Replace `libranet` with your chosen service name)

---

## 🔧 Troubleshooting

### Database Connection Error
- Make sure `SQLALCHEMY_DATABASE_URI` uses the **Internal Database URL** from Render PostgreSQL
- Check the URL format: `postgresql://user:password@host:port/database`

### App Won't Start
- Check logs in Render dashboard
- Common issues:
  - Missing environment variables
  - Database not migrated
  - Import errors in code

### Slow First Load
- Free tier apps sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- Subsequent requests are fast

---

## 💰 Alternative Free Platforms

### Railway (Recommended Alternative)
- **Free Credit**: $5/month
- **Steps**: Similar to Render
- **URL**: https://railway.app
- **Pros**: Faster cold starts

### Fly.io
- **Free Tier**: 3 small VMs
- **URL**: https://fly.io
- **Pros**: Global deployment

### PythonAnywhere
- **Always Free**: Limited resources
- **URL**: https://www.pythonanywhere.com
- **Con**: MySQL only (requires code changes)

---

## 📝 Post-Deployment Checklist

- [ ] Test user registration
- [ ] Test login/logout
- [ ] Test database operations
- [ ] Configure custom domain (optional)
- [ ] Set up monitoring
- [ ] Test email functionality
- [ ] Test file uploads (if any)
- [ ] Test payment gateway (if configured)

---

## 🔒 Security Tips

1. **Never commit `.env` file** to GitHub
2. Use strong `SECRET_KEY` in production
3. Enable HTTPS (Render does this automatically)
4. Set `FLASK_ENV=production`
5. Use Gmail App Passwords (not your actual password)

---

## 📧 Email Setup (Gmail)

1. Go to Google Account Settings
2. Enable 2-Factor Authentication
3. Generate App Password:
   - Settings → Security → 2-Step Verification → App Passwords
4. Use this password for `MAIL_PASSWORD`

---

## 🎯 Quick Deploy Summary

```bash
# 1. Prepare files (already done)
git add Procfile runtime.txt requirements.txt
git commit -m "Add deployment config"
git push

# 2. Create Render account → render.com
# 3. Create PostgreSQL database (Free)
# 4. Create Web Service (Free)
# 5. Add environment variables
# 6. Deploy automatically
# 7. Run migrations via Shell
# 8. Visit your app URL!
```

---

## 🆘 Need Help?

- **Render Docs**: https://render.com/docs
- **Flask Deployment**: https://flask.palletsprojects.com/en/latest/deploying/
- **Check Logs**: Dashboard → Your Service → Logs

---

**Your app is now live on the internet! 🚀**

Free tier limitations:
- Apps sleep after 15 min inactivity
- 750 hours/month (good for 1 app)
- 512 MB RAM
- Perfect for development/portfolio projects
