from __future__ import print_function
import os, datetime, zoneinfo
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

# 1) Point to your credentials.json safely (no escape issues)
CLIENT_PATH = Path(r"C:\Users\gatsi\Box\MY BREATHTAKING PROJECT\Voice Calendar AI\credentials.json")
if not CLIENT_PATH.exists():
    raise FileNotFoundError(f"credentials.json not found at: {CLIENT_PATH}")

# 2) Choose a clear token location (outside your repo is fine)
TOKEN_PATH = Path.home() / ".voice-calendar-ai" / "token.json"
TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_service():
    creds = None
    print(f"🔎 Token path: {TOKEN_PATH}")
    if TOKEN_PATH.exists():
        print("✅ Found token.json; loading credentials…")
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    else:
        print("ℹ️ No token.json yet; first-time consent expected.")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("🔄 Access token expired; refreshing with refresh token…")
            creds.refresh(Request())
        else:
            print(f"🌐 Launching browser for consent using {CLIENT_PATH} …")
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_PATH), SCOPES)
            # fixed port helps on Windows sometimes
            creds = flow.run_local_server(port=8080, prompt="consent",
                                          authorization_prompt_message="Please authorize access in your browser…")

        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
        print(f"💾 Saved new token to {TOKEN_PATH}")

    print("🧩 Building Calendar service…")
    return build("calendar", "v3", credentials=creds)

if __name__ == "__main__":
    service = get_service()

    # Example: tomorrow 10–11 AM America/New_York
    tz = zoneinfo.ZoneInfo("America/New_York")
    now = datetime.datetime.now(tz)
    start_dt = (now + datetime.timedelta(days=3)).replace(hour=3, minute=0, second=0, microsecond=0)
    end_dt   = start_dt + datetime.timedelta(hours=3)

    event = {
        "summary": "API Demo Event",
        "description": "Created via Google Calendar API (OAuth 2.0)",
        "start": {"dateTime": start_dt.isoformat(), "timeZone": "America/New_York"},
        "end":   {"dateTime": end_dt.isoformat(),   "timeZone": "America/New_York"},
    }

    print("📨 Calling events.insert (POST)…")
    created = service.events().insert(
        calendarId="primary",
        body=event,
        sendUpdates="all"
        # ← only include conferenceDataVersion if you set conferenceData in the body
    ).execute()

    print("✅ Event link:", created.get("htmlLink"))
    print("🆔 Event ID:", created.get("id"))
