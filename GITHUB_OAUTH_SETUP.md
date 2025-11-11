# GitHub OAuth Setup Guide for LibraNet

This guide will help you set up GitHub OAuth authentication for your LibraNet application.

## Prerequisites
- A GitHub account
- LibraNet application running

## Step 1: Create a GitHub OAuth App

1. **Go to GitHub Developer Settings**
   - Navigate to: https://github.com/settings/developers
   - Or: GitHub → Settings → Developer settings → OAuth Apps

2. **Create New OAuth App**
   - Click on "New OAuth App" button
   - Fill in the application details:

### Application Details

| Field | Value |
|-------|-------|
| **Application name** | LibraNet |
| **Homepage URL** | `http://localhost:8080` (for development)<br>or your production URL |
| **Application description** | Digital Library Management System |
| **Authorization callback URL** | `http://localhost:8080/auth/github/callback` |

> **Note:** For production, replace `localhost:8080` with your actual domain.

3. **Register Application**
   - Click "Register application"
   - You'll be redirected to your app's settings page

## Step 2: Get Your Credentials

After creating the OAuth app, you'll see:

1. **Client ID** - A public identifier for your app
2. **Client Secret** - Click "Generate a new client secret" to create one

> ⚠️ **Important:** Save your Client Secret immediately. GitHub will only show it once!

## Step 3: Configure LibraNet

1. **Update your `.env` file**

Add these lines to your `.env` file in the LibraNet root directory:

```env
# GitHub OAuth Configuration
GITHUB_OAUTH_CLIENT_ID=your_github_client_id_here
GITHUB_OAUTH_CLIENT_SECRET=your_github_client_secret_here
```

Replace `your_github_client_id_here` and `your_github_client_secret_here` with the actual values from GitHub.

2. **Example `.env` file**

```env
# Database
SQLALCHEMY_DATABASE_URI=mysql://root:password@localhost/libranet

# Flask
SECRET_KEY=your-secret-key-here

# Google OAuth
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret

# GitHub OAuth
GITHUB_OAUTH_CLIENT_ID=Iv1.a1b2c3d4e5f6g7h8
GITHUB_OAUTH_CLIENT_SECRET=abcdef1234567890abcdef1234567890abcdef12

# Email Configuration
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Razorpay
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxx
```

## Step 4: Restart Your Application

```bash
# Stop the current server (Ctrl+C)
# Restart the server
source venv/bin/activate
python main.py
```

## Step 5: Test GitHub OAuth

1. **Navigate to Login/Register page**
   - Go to: `http://localhost:8080/login` or `http://localhost:8080/register`

2. **Click "Continue with GitHub"**
   - You'll be redirected to GitHub's authorization page
   - GitHub will ask you to authorize LibraNet
   - Click "Authorize"

3. **First-Time Users**
   - A new account will be created automatically
   - Your GitHub email and name will be used
   - A unique roll number will be generated (format: `GITHUB-XXXX`)

4. **Returning Users**
   - You'll be logged in automatically
   - No need to enter email/password

## Production Setup

For production deployment, update your GitHub OAuth app with:

1. **Homepage URL**: `https://yourdomain.com`
2. **Authorization callback URL**: `https://yourdomain.com/auth/github/callback`

## Troubleshooting

### "GitHub authentication failed: No verified email found"

**Solution:** 
- Go to GitHub Settings → Emails
- Make sure you have at least one verified email
- Set your primary email to public (optional)

### "redirect_uri_mismatch" Error

**Solution:**
- Check that your callback URL in GitHub OAuth app settings exactly matches: `http://localhost:8080/auth/github/callback`
- No trailing slash
- Correct protocol (http vs https)

### "Application not configured" Error

**Solution:**
- Verify that `GITHUB_OAUTH_CLIENT_ID` and `GITHUB_OAUTH_CLIENT_SECRET` are correctly set in `.env`
- Restart the Flask application after updating `.env`

## Security Notes

- ✅ Never commit your `.env` file to version control
- ✅ Use different OAuth apps for development and production
- ✅ Regenerate client secrets periodically
- ✅ For production, always use HTTPS
- ✅ Keep your client secret confidential

## Features

✨ **What GitHub OAuth Provides:**

- **No Password Required**: Users don't need to create/remember another password
- **Email Verified**: GitHub emails are already verified
- **Quick Signup**: One-click account creation
- **Secure**: OAuth tokens are more secure than storing passwords
- **Automatic Login**: Returning users are logged in automatically

## Support

If you encounter issues:
1. Check GitHub OAuth app settings
2. Verify `.env` configuration
3. Check Flask application logs
4. Review callback URL configuration

---

**Created for LibraNet - Digital Library Management System**
**Team:** TeamX (Vansaj Rawat, Mansi Daramwal, Kritika Basera)
**Mentor:** Mr. Kapil Rajput
