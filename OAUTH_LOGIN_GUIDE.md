# Epidemic Sound OAuth Login Guide

## 🔐 **Google OAuth Login (Updated!)**

Your browser automation now supports Google OAuth! Here's how it works:

---

## 🚀 **Quick Start:**

### **Step 1: Run Login Script**
```bash
python epidemic_oauth_login.py
```

### **Step 2: Complete OAuth in Browser**

**The script will:**
1. ✅ Open Chromium browser automatically
2. ✅ Navigate to Epidemic Sound login page
3. ✅ Wait for you to login

**You need to:**
1. Click **"Sign in with Google"** button in the browser
2. Select your Google account
3. Complete the OAuth flow
4. Wait for redirect back to Epidemic Sound

### **Step 3: Session Saved!**

**After successful login:**
- ✅ Session automatically saved to `epidemic_session.json`
- ✅ Valid for 7 days
- ✅ Future runs don't require login
- ✅ Browser closes automatically after 5 seconds

---

## 📋 **Complete Workflow:**

```bash
# 1. First-time login (one-time, ~30 seconds)
python epidemic_oauth_login.py

# 2. Test session works
python epidemic_oauth_login.py --test

# 3. Run automation (uses saved session)
python epidemic_auto_downloader.py --quick
```

---

## 🎯 **What Happens:**

### **During Login:**
```
[00:00:00] Launching browser...
[00:00:01] Opening Epidemic Sound login page...

================================================================================
EPIDEMIC SOUND LOGIN
================================================================================

The browser window is now open at the Epidemic Sound login page.

PLEASE:
1. Click 'Sign in with Google' button
2. Complete the Google OAuth flow in the browser
3. Wait for redirect back to Epidemic Sound

The automation will detect when you're logged in and continue...
================================================================================

[00:00:45] Login detected!
[00:00:45] ✓ Login successful!
[00:00:45] Saving session for future use...
[00:00:45] Session saved to: epidemic_session.json
[00:00:45] Session valid for: 7 days

================================================================================
SESSION SAVED!
================================================================================

You can now use the automation scripts without logging in again!
Future runs will reuse this session automatically.

[00:00:50] Browser will close in 5 seconds...
```

### **Future Runs (Automatic):**
```
[00:00:00] Valid session found
[00:00:00] Starting automation with saved session...
[00:00:01] Downloading tracks...
```

**No login needed for 7 days!**

---

## ⚡ **No Password Needed!**

**Your `.env.local` only needs email:**
```bash
EPIDEMIC_EMAIL=jdmallin25x40@gmail.com
# EPIDEMIC_PASSWORD not needed for OAuth!
```

---

## 🔄 **Session Management:**

### **Test Session:**
```bash
python epidemic_oauth_login.py --test
```

**Output:**
```
✓ Session is valid!
```
OR
```
✗ Session invalid or expired
```

### **Refresh Session:**
If expired, just run login again:
```bash
python epidemic_oauth_login.py
```

### **Clear Session:**
```bash
del epidemic_session.json
```

---

## 🚀 **NOW RUN THE FULL AUTOMATION:**

```bash
# Quick test (2 tracks, 10 minutes)
python epidemic_auto_downloader.py --quick

# Full download (35 tracks, 2-3 hours)
python epidemic_auto_downloader.py
```

**The automation will:**
- ✅ Use your saved OAuth session
- ✅ No manual login needed
- ✅ Download all music automatically
- ✅ Organize by platform
- ✅ Save metadata

---

## 💡 **Benefits of OAuth:**

- ✅ **Safer** (no password stored)
- ✅ **More reliable** (Google handles auth)
- ✅ **2FA compatible** (if you use it)
- ✅ **Session lasts 7 days**
- ✅ **One-click login** (select Google account)

---

## 📝 **Complete Commands:**

```bash
# 1. LOGIN (first time only)
python epidemic_oauth_login.py

# 2. TEST (verify session)
python epidemic_oauth_login.py --test

# 3. DOWNLOAD MUSIC
python epidemic_auto_downloader.py --quick

# 4. VIEW LIBRARY
python show_music_library.py --stats
```

---

## ✅ **YOU'RE READY!**

**Run this now:**
```bash
python epidemic_oauth_login.py
```

**Then:**
1. Click "Sign in with Google" in the browser
2. Select your account
3. Wait for session to save
4. Run: `python epidemic_auto_downloader.py --quick`

**Done!** 🎵🤖
