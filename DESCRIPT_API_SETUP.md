# Descript API Setup Guide

## How to Get Your API Key

### THE CORRECT WAY: Contact Descript Directly

You **must contact Descript** - there's no self-service API key generation.

**Step 1: Email Descript Support**

```
To: support@descript.com
Or: API request form at https://www.descript.com/contact

Subject: Request API Access - Personal Token

Body:
"I have a $30/month Descript account and need to enable API access for my video automation project. Can you provide my personal API token?"
```

**Step 2: Include Your Info**

- Your Descript account email
- What you're using the API for (video generation, automation)
- Any relevant details

**Step 3: They'll Send Your Token**

- Wait 24-48 hours for response
- They'll send your personal token via email
- Token format: `descript_sk_xxxxxxxxxxxxxxxxxxxxx` (or similar)

**Step 4: Add to .env**

```bash
# Edit .env
nano .env

# Add:
DESCRIPT_API_KEY=descript_sk_YOUR_TOKEN_FROM_EMAIL
```

### Alternative: Use Contact Form

Go to: https://www.descript.com/contact

Select: **API Access Request** or **Business Inquiry**

Message: "I need API access for my $30 plan. Can you provide a personal token?"

## What Your API Key Should Look Like

```
descript_sk_xxxxxxxxxxxxxxxxxxxxx
or
your-api-key-hash-here
```

## Verify Your Token Works

Once you have it, add to `.env`:

```bash
DESCRIPT_API_KEY=your_actual_token_here
```

Then test:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://descriptapi.com/v1/user/profile
```

If you get a response, your token works!

## Security Notes

⚠️ IMPORTANT:
- Never commit `.env` to git
- Keep your token secret
- Rotate tokens periodically
- Each token is unique to your account

## Next Steps

Once you have the API key:
1. Add to `.env` as `DESCRIPT_API_KEY`
2. Run: `node descript-video-editor.js`
3. System will use Descript instead of previous TTS/video methods
