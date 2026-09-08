import os
import time
from datetime import datetime, timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def get_calendar_service():
    """Authenticate with Google Calendar and return an API service."""
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists("credentials.json"):
                raise FileNotFoundError(
                    "credentials.json was not found. Add your Google OAuth desktop "
                    "credentials locally; never commit this file."
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


def list_upcoming_events(max_results=10):
    """Return upcoming events from the user's primary calendar."""
    service = get_calendar_service()
    now = datetime.now(timezone.utc).isoformat()

    result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute(num_retries=2)
    )

    events = []
    for event in result.get("items", []):
        events.append(
            {
                "id": event.get("id"),
                "summary": event.get("summary", "No title"),
                "start": event.get("start", {}).get(
                    "dateTime", event.get("start", {}).get("date")
                ),
                "end": event.get("end", {}).get(
                    "dateTime", event.get("end", {}).get("date")
                ),
                "html_link": event.get("htmlLink"),
            }
        )

    return {"status": "success", "events": events}


def create_calendar_event(
    summary,
    start_datetime,
    end_datetime,
    timezone_name="Asia/Riyadh",
):
    """Create a calendar event. The caller must obtain human approval first."""
    service = get_calendar_service()

    event = {
        "summary": summary,
        "start": {"dateTime": start_datetime, "timeZone": timezone_name},
        "end": {"dateTime": end_datetime, "timeZone": timezone_name},
    }

    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            created_event = (
                service.events()
                .insert(calendarId="primary", body=event)
                .execute(num_retries=2)
            )
            return {
                "status": "success",
                "event_id": created_event.get("id"),
                "html_link": created_event.get("htmlLink"),
                "summary": created_event.get("summary"),
            }
        except (ConnectionResetError, TimeoutError, HttpError) as error:
            if attempt < max_attempts - 1:
                wait_time = 3 * (attempt + 1)
                print(
                    f"\nCalendar request failed. Retrying in {wait_time} seconds..."
                )
                time.sleep(wait_time)
            else:
                return {
                    "status": "error",
                    "message": f"Google Calendar request failed: {error}",
                }
