import os
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timezone

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]


def get_calendar_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(
                port=0
            )

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    return service


def create_calendar_event(
    summary,
    start_datetime,
    end_datetime,
    timezone_name="Asia/Riyadh"
):
    service = get_calendar_service()

    event = {
        "summary": summary,
        "start": {
            "dateTime": start_datetime,
            "timeZone": timezone_name,
        },
        "end": {
            "dateTime": end_datetime,
            "timeZone": timezone_name,
        },
    }

    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            created_event = (
                service.events()
                .insert(
                    calendarId="primary",
                    body=event
                )
                .execute()
            )

            return {
                "status": "success",
                "event_id": created_event.get("id"),
                "html_link": created_event.get("htmlLink"),
                "summary": created_event.get("summary"),
            }

        except ConnectionResetError:
            if attempt < max_attempts - 1:
                wait_time = 3 * (attempt + 1)

                print(
                    f"\nCalendar connection interrupted. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                return {
                    "status": "error",
                    "message": (
                        "Could not connect to Google Calendar "
                        "after multiple attempts."
                    )
                }