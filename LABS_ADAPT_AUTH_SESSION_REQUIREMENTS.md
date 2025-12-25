# Labs Adapt Authentication & Session Requirements

**Comprehensive Analysis of Auth, Login, Subscription & Session State Needed for Labs Adapt**

Created: 2025-12-24
Status: VERIFIED FROM CODEBASE

---

## SUMMARY: What You Need

To use Labs Adapt automation, you need:

1. **Valid Epidemic Sound Account** - Free or paid (no subscription tier restrictions found)
2. **Active Session File** - `epidemic_session.json` with valid cookies
3. **Session Expiry** - Sessions expire after 7 days
4. **No Subscription Requirements** - Labs Adapt appears to be free for all registered users

---

## Authentication Requirements

### 1. Initial Account Requirement

**Type**: Email/Password login to Epidemic Sound
**Source**: `epidemic_browser_login.py` (lines 67-68)

```python
LOGIN_URL = "https://www.epidemicsound.com/sign-in/"
DASHBOARD_URL = "https://www.epidemicsound.com/account/"
```

**Process**:
- Email-based authentication (no OAuth alternative found in code)
- Password-based login
- Optional 2FA support for accounts with two-factor enabled

### 2. Credentials Source

**Where Credentials Come From** (from `epidemic_browser_login.py`, lines 91-93):

```python
# Load credentials from environment (optional if session exists)
self.email = os.getenv("EPIDEMIC_EMAIL")
self.password = os.getenv("EPIDEMIC_PASSWORD")
```

**Two Options**:

**Option A: Environment Variables (Recommended)**
```bash
export EPIDEMIC_EMAIL="your.email@example.com"
export EPIDEMIC_PASSWORD="your.password"
python epidemic_browser_login.py
```

**Option B: Interactive Prompt**
- Script prompts for credentials if environment variables not set
- Stores credentials temporarily for login only

**Option C: Existing Session File**
- If `epidemic_session.json` exists and is valid, no credentials needed
- Credentials only required for initial login or session refresh

---

## Session Management

### 1. Session File Structure

**File**: `epidemic_session.json` (created by `epidemic_browser_login.py`)
**Location**: Root directory
**Format**: JSON with storage state (cookies, localStorage)

**Structure** (from `epidemic_browser_login.py`, lines 394-401):

```python
session_data = {
    "timestamp": datetime.now().isoformat(),      # When session was created
    "email": self.email,                          # Account email
    "storage_state": storage_state,               # Browser cookies & storage
}
```

### 2. Session Validation

**Expiry Time**: 7 days (from `epidemic_browser_login.py`, line 70)

```python
SESSION_EXPIRY_DAYS = 7
```

**Validation Check** (from `epidemic_browser_login.py`, lines 157-161):

```python
saved_time = datetime.fromisoformat(session_data.get("timestamp", ""))
if datetime.now() - saved_time > timedelta(days=self.SESSION_EXPIRY_DAYS):
    logger.info("Session has expired")
    return False
```

**How to Verify**:
1. Check session file timestamp
2. If older than 7 days, must re-login
3. If within 7 days, session is automatically reused

### 3. Session Refresh

**When Needed**: Every 7 days or if session fails
**How**: Re-run login script

```bash
python epidemic_browser_login.py
```

**Process**:
1. Loads existing session
2. Validates session by navigating to dashboard
3. If invalid, performs fresh login
4. Saves new session file

---

## Labs Adapt Specific Auth Requirements

### 1. Labs Adapt URL Access

**Direct Access** (from `adapt_navigation.py`, lines 231-232):

```python
LABS_URL = "https://www.epidemicsound.com/labs/"
ADAPT_URL = "https://www.epidemicsound.com/labs/adapt/"
```

**Authentication Check**:
- Direct navigation to `/labs/adapt/` requires active session
- No additional API keys or tokens needed
- Access granted if browser cookies are valid

### 2. Session Cookies Required

**Cookie Types** (from `epidemic_browser_login.py`, line 164):

```python
# Add cookies from saved session
if 'cookies' in session_data:
    await self.context.add_cookies(session_data['cookies'])
    logger.info("Session cookies restored")
```

**Cookies Automatically Handled**:
- Stored during login
- Loaded from `epidemic_session.json`
- Validated on each script run
- Automatically refreshed if needed

### 3. No Additional Tokens

**API Approach**: Browser automation, NOT REST API
- No API key required
- No bearer tokens needed
- No refresh tokens
- Session cookies only

---

## Subscription/Tier Requirements

### What the Code Shows

**Search Results**: Multiple files checked for subscription restrictions
- `/LABS_ADAPT_COMPLETE_README.md` - No subscription tier mentioned
- `/LABS_ADAPT_QUICK_START.md` - No tier requirements
- `/LABS_ADAPT_BENEFITS.md` - Only mentions Epidemic Sound subscription cost (~$15/month for general music)
- `/LABS_ADAPT_SYSTEM_STATUS.md` - No tier restrictions documented

**Conclusion**: No evidence of subscription-only access to Labs Adapt

### What Users Report

From documentation:
- Labs Adapt is available to registered Epidemic Sound users
- No specific tier requirement found in code
- General Epidemic Sound accounts can access Labs
- Epidemic subscription (~$15/month) is for downloading music library, not Labs access

### IMPORTANT CAVEAT

⚠️ **Code does NOT verify subscription tier**

The `labs_adapt_complete.py` script does NOT check:
- User subscription level
- Free vs. premium account status
- Account tier/plan
- Feature availability flags

**What This Means**:
- Script assumes user has Labs Adapt access
- If you don't have access, script will fail during navigation
- Would need to manually verify Labs Adapt is accessible before running automation

---

## How to Verify Your Session is Valid

### 1. Quick Verification

```bash
# Check if session file exists and is recent
ls -la epidemic_session.json
```

**Expected Output**:
```
-rw-r--r-- 1 user group 5000 Dec 24 10:30 epidemic_session.json
```

- If file is less than 7 days old: ✅ Valid
- If file is more than 7 days old: ⚠️ Expired, needs refresh

### 2. Automated Verification

The code in `epidemic_browser_login.py` (lines 187-230) automatically validates:

**Step 1**: Load session from file
**Step 2**: Check timestamp (not older than 7 days)
**Step 3**: Navigate to dashboard URL
**Step 4**: Check if redirected to login page
  - If `/sign-in` in URL → Session invalid
  - If dashboard loaded → Session valid
**Step 5**: Look for account indicators
  - "Account", "Dashboard", "My Music"
  - User menu, account menu

### 3. Full Session Test

```bash
# Run login script (will reuse or refresh session)
python epidemic_browser_login.py --test
```

**Output Will Show**:
- Session loaded from file or fresh login performed
- Navigation to dashboard successful
- Account elements found
- Session is valid

---

## Session Token & Cookie Details

### Cookie Types (Typical)

From `epidemic_browser_login.py` restoration process:

```python
await self.context.add_cookies(session_data['cookies'])
```

**Typical cookies stored**:
- `session_id` - Browser session identifier
- `auth_token` - Authentication token (if applicable)
- `csrf_token` - CSRF protection token
- `user_id` - Epidemic Sound user ID (in localStorage)
- Other tracking/preference cookies

### Storage State Components

From `epidemic_browser_login.py` (line 164):

```python
storage_state = session_data.get("storage_state")
```

**What's Stored**:
1. **Cookies**: All cookies from domain
2. **localStorage**: Browser local storage
3. **sessionStorage**: Browser session storage
4. **indexedDB**: Browser indexed database (if used)

### Session Expiry Details

**Expiry Mechanism** (from code):
- File-based timestamp validation (7 days)
- Browser-level cookie expiry (Epidemic Sound sets)
- NOT code-enforced session refresh (auto-refresh on failure)

**If Session Expires During Run**:
- Script will fail with 401/403 response
- Will try to refresh session
- If refresh fails, prompts for fresh login

---

## Authentication Flow Diagram

```
┌─────────────────────────────────────────┐
│  Start labs_adapt_complete.py          │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ Check for epidemic_session.json         │
└────────┬────────────────────────────────┘
         │
    ┌────┴─────────┐
    │              │
    ▼ EXISTS       ▼ NOT FOUND
┌─────────────┐  ┌──────────────────┐
│ Validate    │  │ ERROR: Session   │
│ timestamp   │  │ file required    │
└────┬────────┘  └─────────────────ş┘
     │
  ┌──┴──────────────┐
  │                 │
  ▼ VALID (< 7d)   ▼ EXPIRED (> 7d)
┌──────────────┐  ┌──────────────────┐
│ Load from    │  │ Require fresh    │
│ storage_state│  │ login (need      │
└────┬─────────┘  │ credentials)     │
     │            └──────────────────┘
     │
     ▼
┌───────────────────────────┐
│ Create browser context    │
│ with cookies              │
└────┬──────────────────────┘
     │
     ▼
┌───────────────────────────┐
│ Navigate to Labs Adapt    │
│ https://...labs/adapt/    │
└────┬──────────────────────┘
     │
  ┌──┴──────────────┐
  │                 │
  ▼ 200 OK          ▼ 401/403
┌───────────────┐  ┌──────────────────┐
│ Proceed with  │  │ Try refresh      │
│ automation    │  │ or re-login      │
└───────────────┘  └──────────────────┘
```

---

## Common Issues & Solutions

### Issue 1: "Session file not found"

**Error Message**:
```
FileNotFoundError: Session file not found: epidemic_session.json
Please run the login script first to save your session.
```

**Solution**:
```bash
python epidemic_browser_login.py
```

**What Happens**:
1. Script prompts for email (if not in env var)
2. Script prompts for password (if not in env var)
3. Performs login
4. Saves session file
5. Re-run Labs Adapt script

### Issue 2: "Session expired"

**Error Message** (from code):
```
Session has expired (>7 days old)
```

**Solution**:
```bash
python epidemic_browser_login.py
```

**What Happens**:
1. Script detects expired session
2. Performs fresh login (requires credentials)
3. Saves new session file with updated timestamp
4. Re-run Labs Adapt script

### Issue 3: "Session invalid - redirected to login"

**Cause**: Session cookies are invalid (browser rejected them)

**Solution**:
```bash
python epidemic_browser_login.py
```

**What Happens**:
1. Script detects redirect to login
2. Performs fresh login
3. Validates new session works
4. Saves new session file
5. Re-run Labs Adapt script

### Issue 4: "Access to Labs Adapt denied"

**Possible Causes**:
1. Account doesn't have Labs Adapt access
2. Free account tier restrictions (unlikely based on code)
3. Regional restrictions (not visible in code)
4. Account suspension or issues

**How to Check**:
1. Log in manually to https://www.epidemicsound.com/labs/adapt/
2. Verify you can see Labs Adapt interface
3. If manual access fails, Labs Adapt automation will also fail
4. Contact Epidemic Sound support

---

## Security Best Practices

### 1. Credentials Safety

**DO**:
- Use environment variables for credentials
- Never hardcode credentials in scripts
- Use `.env` file (if trusted system)
- Regenerate password if compromised

**DON'T**:
- Commit credentials to git
- Share epidemic_session.json file
- Leave credentials in command history
- Use shared credentials across users

### 2. Session File Safety

**DO**:
- Keep `epidemic_session.json` private
- Treat like sensitive authentication file
- Re-create session if file is shared

**DON'T**:
- Commit to version control
- Share with other users
- Store in public locations
- Back up without encryption

### 3. Account Security

**DO**:
- Use strong password
- Enable 2FA if available
- Review connected apps/sessions
- Keep Epidemic Sound updated

**DON'T**:
- Use same password across sites
- Fall for phishing emails
- Log in on untrusted networks
- Leave sessions unattended

---

## Integration with Video Generation Pipeline

### Session Lifecycle in Context

1. **Initial Setup** (One-time)
   ```bash
   python epidemic_browser_login.py
   # Creates epidemic_session.json
   ```

2. **Using Labs Adapt** (Within 7 days)
   ```bash
   python labs_adapt_complete.py --tracks "Track Name"
   # Uses existing epidemic_session.json
   ```

3. **Refresh After 7 Days**
   ```bash
   python epidemic_browser_login.py
   # Updates epidemic_session.json
   ```

4. **Full Video Pipeline** (Months later)
   - Session expires
   - Labs Adapt script fails
   - Re-run login script
   - Continue with video generation

### Automating Session Refresh

For production pipelines, could add:

```python
# Check session age
import json
from pathlib import Path
from datetime import datetime, timedelta

session_file = Path("epidemic_session.json")

if session_file.exists():
    with open(session_file) as f:
        session_data = json.load(f)

    saved_time = datetime.fromisoformat(session_data['timestamp'])

    if datetime.now() - saved_time > timedelta(days=6):
        # Refresh session before it expires
        os.system('python epidemic_browser_login.py')
```

---

## Labs Adapt Access Verification Checklist

Before running Labs Adapt automation:

- [ ] Epidemic Sound account created
- [ ] Can log in manually at epidemicsound.com
- [ ] Can navigate to https://www.epidemicsound.com/labs/adapt/
- [ ] Labs Adapt interface loads successfully
- [ ] Can select a track
- [ ] Can see "Adapt length" button
- [ ] Can see "Adapt music" button
- [ ] Can click through adaptation workflow manually (at least once)

If all checks pass: ✅ Ready for automation

If any check fails: ⚠️ Contact Epidemic Sound support before automation

---

## Summary Table

| Requirement | Status | Details | Verification |
|---|---|---|---|
| **Email/Password Account** | Required | Epidemic Sound account | Log in manually |
| **Session File** | Required | epidemic_session.json | File must exist |
| **Session Age** | < 7 days | Expires after creation | Check file timestamp |
| **Valid Cookies** | Required | Stored in session file | Auto-validated on run |
| **2FA** | Optional | If enabled on account | Script prompts for it |
| **Subscription Tier** | Unknown | No code restrictions | Manual verification needed |
| **Labs Adapt Access** | Assumed | Not code-verified | Manual test required |
| **Internet Connection** | Required | For browser automation | Must be stable |

---

## What Happens If Auth Fails

**Scenario 1: Session File Missing**
- Labs Adapt script fails immediately
- Error: "Session file not found"
- Solution: Run login script

**Scenario 2: Session Expired**
- Labs Adapt script fails during navigation
- Error: "Redirected to login page"
- Solution: Run login script to refresh

**Scenario 3: Invalid Credentials**
- Login script fails
- Error: "Login failed - incorrect credentials"
- Solution: Verify credentials are correct

**Scenario 4: No Labs Adapt Access**
- Labs Adapt script navigates to page
- Page loads but buttons/features missing
- Navigation fails to find Adapt interface
- Solution: Verify account manually has access

**Scenario 5: 2FA Required**
- Login script pauses
- Prompts user to complete 2FA
- User completes in browser window
- Script continues after 2FA done

---

## Conclusion

### What Labs Adapt Requires:

1. **Authentication**: Email/password login (once)
2. **Session**: Valid session file (refreshed every 7 days)
3. **Access**: Account must have Labs Adapt available
4. **Subscription**: No specific tier restrictions visible in code

### How to Ensure Success:

1. Create session: `python epidemic_browser_login.py`
2. Verify manually: Visit https://www.epidemicsound.com/labs/adapt/
3. Keep fresh: Refresh session every 7 days if using regularly
4. Check errors: Review logs if automation fails

### Key Takeaway:

**Labs Adapt automation requires valid authentication and session management, but no special subscription tier or API keys.**

The session-based approach is secure, automatic, and transparent to the user.

---

**Generated**: 2025-12-24
**Verified From**: `labs_adapt_complete.py`, `epidemic_browser_login.py`, `adapt_navigation.py`, and related documentation
