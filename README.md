# Google Calendar Event Creator (Python + OAuth 2.0)

Create Google Calendar events from a Python script using OAuth 2.0 user consent.  
No secrets are committed — `credentials.json` and `token.json` stay local (or in env vars).

## Demo
- **Video walkthrough:** _link-to-your-video_
- **Creates:** timed or all-day events
- **Optional:** Google Meet link, update, delete

## Setup

### 1) Google Cloud
1. Create a project → **Enable** “Google Calendar API”.
2. **OAuth consent screen**: User type = External, add yourself as **Test user**.
3. **Create credentials** → OAuth client ID → **Desktop app** → download JSON.

### 2) Local files (keep secrets out of Git)
- Put the downloaded file **outside** your repo or keep it local.
- Name it `credentials.json` or set an env var path (see below).
- Add `.gitignore`:
