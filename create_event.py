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
