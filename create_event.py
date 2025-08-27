from __future__ import print_function
import os, datetime, zoneinfo
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

def get_service():
    creds = None                                 # 1) Start with no credentials in memory.

    if os.path.exists("token.json"):             # 2) If we previously authorized, a token file exists...
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
                                                 #    ...load tokens (access + refresh + expiry + scopes) into 'creds'.

    if not creds or not creds.valid:             # 3) If we have no creds OR the loaded creds are not valid:
        if creds and creds.expired and creds.refresh_token:
                                                 # 4) If creds exist AND the access token is expired AND we have a refresh token:
            creds.refresh(Request())             #    -> silently get a new access token via the refresh token.
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                                                 # 5) Otherwise, kick off the OAuth flow using your client config...
            creds = flow.run_local_server(port=0)#    ...opens a browser, you sign in & Allow, Google returns fresh tokens.

        with open("token.json", "w") as f:       # 6) Persist whatever 'creds' we now have (new or refreshed) to disk...
            f.write(creds.to_json())             #    ...so next run can skip the browser.

    return build("calendar", "v3", credentials=creds)
                                                 # 7) Build a Calendar API client bound to these creds.

if __name__ == "__main__":
    service = get_service()

    # Example: tomorrow 10–11 AM America/New_York
    tz = zoneinfo.ZoneInfo("America/New_York")
    now = datetime.datetime.now(tz)
    start_dt = (now + datetime.timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)
    end_dt   = start_dt + datetime.timedelta(hours=1)

    event = {
        "summary": "API Demo Event",
        "description": "Created via Google Calendar API (OAuth 2.0)",
        "start": {"dateTime": start_dt.isoformat(), "timeZone": "America/New_York"},
        "end":   {"dateTime": end_dt.isoformat(),   "timeZone": "America/New_York"},
        # Optional examples:
        # "attendees": [{"email": "friend@example.com"}],
        # "location": "Library Room 2",
        # "reminders": {"useDefault": True},
        # "conferenceData": {"createRequest": {"requestId": "unique-id-123"}},  # adds Google Meet link
    }

    print("Creating event…")
    created = service.events().insert(
        calendarId="primary",
        body=event,
        sendUpdates="all",            # email guests if you add attendees
        conferenceDataVersion=1       # needed only if you included conferenceData above
    ).execute()

    print("✅ Event link:", created.get("htmlLink"))
    print("🆔 Event ID:", created.get("id"))
    # If you added conferenceData:
    # print("🔗 Meet:", created.get("hangoutLink"))