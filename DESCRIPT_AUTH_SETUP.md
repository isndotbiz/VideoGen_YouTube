# Descript Authentication Setup

Two ways to authenticate with Descript API.

## Option 1: API Key (Simplest - What You Have Now)

### ✅ Current Status
You already have this set up in `.env`:
```bash
DESCRIPT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

This is a **Direct API Token** (JWT format) - no OAuth needed!

### How It Works
```javascript
const axios = require('axios');

const response = await axios.post(
  'https://descriptapi.com/v1/projects',
  { title: 'My Project' },
  {
    headers: {
      'Authorization': `Bearer ${process.env.DESCRIPT_API_KEY}`,
      'Content-Type': 'application/json'
    }
  }
);
```

### Pros
✅ Simple - just use the token directly
✅ No user login required
✅ Perfect for automation
✅ Already configured in your `.env`

### Cons
❌ Token has expiration (yours expires in 2157 - you're good!)
❌ No user consent flow

### Status Check
```bash
node descript-video-editor.js --test
```

---

## Option 2: OAuth 2.0 (For User-Facing Apps)

### When to Use
- If you want users to connect their own Descript accounts
- If you're building a web app with multiple users
- If you want users to authenticate directly

### NOT Needed For
- Automation (you're doing this)
- Backend processing
- Single user/account setup

### Setup (If You Wanted OAuth)

1. **Register App at Descript:**
   - Go: https://www.descript.com/account/api
   - Create OAuth app
   - Get: `CLIENT_ID` and `CLIENT_SECRET`

2. **Add to .env:**
   ```bash
   DESCRIPT_CLIENT_ID=your_client_id
   DESCRIPT_CLIENT_SECRET=your_client_secret
   DESCRIPT_REDIRECT_URI=http://localhost:8888/callback
   ```

3. **Implement OAuth Flow:**
   ```javascript
   // 1. Redirect user to login
   https://www.descript.com/authorize?client_id=YOUR_ID&redirect_uri=YOUR_URI

   // 2. User logs in and approves
   // 3. Redirect back with authorization code
   // 4. Exchange code for access token
   // 5. Use access token in API calls
   ```

### Complexity
⚠️ Much more complex
⚠️ Requires web server
⚠️ Token refresh management
⚠️ User consent screens

---

## Current Setup: API Key (Recommended)

### Your Current Implementation
```javascript
// descript-video-editor.js
const apiKey = process.env.DESCRIPT_API_KEY;

// Direct API call
await axios.post(
  'https://descriptapi.com/v1/projects',
  schema,
  {
    headers: {
      'x-api-key': apiKey,
      'Content-Type': 'application/json'
    }
  }
);
```

### This is Perfect For:
✅ Automation scripts
✅ Batch processing
✅ Backend pipelines
✅ Your use case (generating videos)

---

## Verify Your API Key

### Check if it's working:
```bash
node descript-video-editor.js --test
```

Expected output:
```
✓ API Key found
✓ Token starts with: eyJhbGciOiJIUzI1NiIs...
Ready to use Descript API!
```

### If it fails:
```bash
# Get new token from:
# https://www.descript.com/account/api
#
# Then update .env:
DESCRIPT_API_KEY=new_token_here
```

---

## API Key vs OAuth Comparison

| Feature | API Key | OAuth |
|---------|---------|-------|
| **Setup Time** | 30 sec | 30 min |
| **Complexity** | Simple | Complex |
| **User Login** | ❌ No | ✅ Yes |
| **Automation** | ✅ Perfect | ⚠️ Works |
| **Permissions** | Full account | User scoped |
| **Token Refresh** | Rarely | Every hour |
| **Best For** | Backend | User apps |

---

## Your Situation

### You Have:
✅ Descript Creator Plan
✅ API Key already in .env
✅ Direct token ready to use
✅ No user login needed

### Use Case:
✅ Batch video generation
✅ Automated pipeline
✅ Single account operation

### Best Choice:
**API Key (what you already have)**

---

## Testing Your Auth

### Method 1: Test Command
```bash
node descript-video-editor.js --test
```

### Method 2: Generate Single Video
```bash
node pipeline-complete.js "https://zapier.com/blog/claude-vs-chatgpt/" --use-descript
```

### Method 3: Debug Mode
Add to `.env`:
```bash
DEBUG=true
```

Then check logs:
```bash
tail -f logs/pipeline-*.log | grep -i descript
```

---

## Troubleshooting Auth Issues

### Error: "Invalid token"
```bash
# Solution: Get fresh token from:
# https://www.descript.com/account/api

# Update .env with new DESCRIPT_API_KEY
# Then test again:
node descript-video-editor.js --test
```

### Error: "DESCRIPT_API_KEY not found"
```bash
# Check .env exists:
cat .env | grep DESCRIPT

# If missing, add it:
DESCRIPT_API_KEY=your_token_here
```

### Error: "Unauthorized (401)"
```bash
# Token expired - get new one:
# https://www.descript.com/account/api

# Or token is invalid - check for typos:
# Make sure full token is in .env (might be cut off)
```

---

## Next Steps

### 1. Verify Current Auth
```bash
node descript-video-editor.js --test
```

### 2. If Working, Generate Video
```bash
node pipeline-complete.js "https://zapier.com/blog/claude-vs-chatgpt/" --use-descript
```

### 3. If Auth Fails
```bash
# Go to: https://www.descript.com/account/api
# Copy new API token
# Update DESCRIPT_API_KEY in .env
# Test again
```

---

## FAQ

**Q: Do I need to set up OAuth?**
A: No! Your API key is perfect for automation.

**Q: Will my token expire?**
A: Yours expires in 2157, so no worries for decades!

**Q: Can I use multiple accounts?**
A: With API key - no. With OAuth - yes (but more complex).

**Q: Is API key secure?**
A: Keep it in .env (never commit to git). It's as secure as any API token.

**Q: Can I revoke the token?**
A: Yes, at https://www.descript.com/account/api

---

## Summary

**You already have everything set up!**

Your API key in `.env` is ready to use. No OAuth needed for your automation use case.

```bash
# Just run this to generate videos:
node pipeline-complete.js "url" --use-descript
```

That's it! The authentication is handled automatically. ✅
