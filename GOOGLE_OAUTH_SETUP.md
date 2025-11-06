# Google OAuth Setup Guide for LibraNet

## ✅ What's Already Done

1. **Backend Integration** - Google OAuth route added (`/auth/google`)
2. **Frontend Button** - Google Sign-In button on registration page
3. **Libraries Installed** - `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`
4. **Configuration** - Config variables added to `config.py`
5. **Email Restriction Removed** - Anyone can register with any email

---

## 🔧 What You Need to Do

### Step 1: Get Google OAuth Credentials (FREE)

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/

2. **Create or Select Project**
   - Click "Select a project" → "New Project"
   - Name: "LibraNet" (or any name)
   - Click "Create"

3. **Configure OAuth Consent Screen**
   - Navigate to: **APIs & Services** → **OAuth consent screen**
   - User Type: Select **External**
   - Click **Create**
   
   Fill in:
   - App name: `LibraNet`
   - User support email: Your email
   - Developer contact: Your email
   - Click **Save and Continue**
   
   Scopes: Click **Save and Continue** (skip, use defaults)
   
   Test users: Click **Save and Continue** (optional for now)

4. **Create OAuth Credentials**
   - Navigate to: **APIs & Services** → **Credentials**
   - Click **+ CREATE CREDENTIALS** → **OAuth 2.0 Client IDs**
   
   Configure:
   - Application type: **Web application**
   - Name: `LibraNet Web Client`
   
   **Authorized JavaScript origins:**
   ```
   http://localhost:8080
   ```
   
   **Authorized redirect URIs:**
   ```
   http://localhost:8080
   http://localhost:8080/auth/google
   ```
   
   Click **CREATE**

5. **Copy Your Credentials**
   - A popup will show your **Client ID** and **Client Secret**
   - **IMPORTANT:** Copy both - you need to add them to `.env`

### Step 2: Update Your `.env` File

Add these lines to `/Users/vansajrawat/Desktop/librafinal/LibraNet/.env`:

```bash
# Google OAuth (paste your actual credentials here)
GOOGLE_OAUTH_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret-here
OAUTHLIB_INSECURE_TRANSPORT=1
```

**Replace:**
- `your-client-id-here` with your actual Client ID
- `your-client-secret-here` with your actual Client Secret

### Step 3: Test It!

1. **Start your server:**
   ```bash
   python3 main.py
   ```

2. **Go to register page:**
   ```
   http://localhost:8080/register
   ```

3. **You should see:**
   - Regular registration form (top)
   - "or continue with" divider
   - **Google Sign-In button** (rendered by Google)

4. **Click Google button:**
   - Select your Google account
   - First time: Creates new LibraNet account automatically
   - Returns: Logs you in and redirects to books page

---

## 🎯 How It Works

### For New Users:
1. Click "Sign in with Google"
2. Select Google account
3. **Account created automatically** with:
   - Name from Google profile
   - Email from Google
   - Auto-generated roll number (GOOGLE-XXXX)
   - Verified status (no OTP needed)
4. Logged in immediately → Books page

### For Existing Users:
1. Click "Sign in with Google"
2. Select Google account
3. System finds existing account by email
4. Logged in immediately → Books page

---

## 🔒 Security Features

- ✅ Token verified with Google servers
- ✅ Email automatically verified (trusted source)
- ✅ Secure random password generated for OAuth users
- ✅ HTTPS enforced in production
- ✅ No password needed for Google users

---

## 📝 Important Notes

### Free Tier:
- **100% FREE** for your use case
- Up to **50,000 monthly active users** free
- No credit card required
- No hidden costs

### Development vs Production:

**Currently (Development):**
- `OAUTHLIB_INSECURE_TRANSPORT=1` allows HTTP
- Works with `http://localhost:8080`

**When deploying (Production):**
1. Remove or set `OAUTHLIB_INSECURE_TRANSPORT=0`
2. Add your production domain to:
   - Authorized JavaScript origins: `https://yourdomain.com`
   - Authorized redirect URIs: `https://yourdomain.com/auth/google`
3. Update `.env` with production URLs

---

## 🐛 Troubleshooting

### "Error 400: redirect_uri_mismatch"
- Check authorized redirect URIs in Google Console
- Must exactly match: `http://localhost:8080`

### "Error 401: invalid_client"
- Double-check Client ID and Secret in `.env`
- Make sure no extra spaces or quotes

### Google button doesn't appear
- Check browser console for errors
- Verify `GOOGLE_OAUTH_CLIENT_ID` is set correctly
- Try hard refresh (Cmd+Shift+R)

### "idna" or import errors
- Run: `pip install google-auth google-auth-oauthlib`

---

## ✨ Features Completed

- ✅ Email domain restriction removed (anyone can register)
- ✅ Google OAuth integration (backend + frontend)
- ✅ Auto-account creation for new Google users
- ✅ Automatic login for existing users
- ✅ No OTP needed for Google sign-ups
- ✅ Chatbot updated to welcome all users
- ✅ Beautiful Google Sign-In button UI

---

## 🎉 You're Almost There!

Just add your Google credentials to `.env` and you're done!

Questions? Check the troubleshooting section above.
