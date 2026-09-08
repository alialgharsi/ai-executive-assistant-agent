import json
import os
import time
from datetime import datetime

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError, ServerError

from tools import add_task, read_text_file, search_knowledge_base, show_tasks


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Copy .env.example to .env and add your key."
    )

client = genai.Client(api_key=api_key)

chat = client.chats.create(
    model="gemini-3.7-flash",
    config=types.GenerateContentConfig(
        tools=[show_tasks, add_task, read_text_file, search_knowledge_base]
    ),
)


def ask_ai(user_input):
    """Send a normal conversational request to Gemini with safe read/write tools."""
    max_attempts = 4

    for attempt in range(max_attempts):
        try:
            response = chat.send_message(user_input)
            return response.text
        except ClientError as error:
            if error.code != 429:
                raise
            wait_time = 15 * (attempt + 1)
            print(f"\nRate limit reached. Waiting {wait_time} seconds...")
            time.sleep(wait_time)
        except ServerError as error:
            if error.code != 503:
                raise
            wait_time = 5 * (attempt + 1)
            print(f"\nGemini is busy. Waiting {wait_time} seconds...")
            time.sleep(wait_time)

    return "The AI service is temporarily unavailable. Please try again later."


def propose_calendar_event(user_input, timezone_name="Asia/Riyadh"):
    """Turn natural-language scheduling text into a proposed event payload.

    This function never writes to Google Calendar. main.py must display the proposal
    and obtain explicit human approval before calling create_calendar_event().
    """
    now = datetime.now().astimezone()
    prompt = f"""
You extract calendar event details for an executive assistant.
Current local datetime: {now.isoformat()}
Default timezone: {timezone_name}

User request:
{user_input}

Return ONLY valid JSON with exactly these keys:
{{
  "is_calendar_request": true,
  "summary": "short event title",
  "start_datetime": "YYYY-MM-DDTHH:MM:SS",
  "end_datetime": "YYYY-MM-DDTHH:MM:SS",
  "timezone_name": "{timezone_name}"
}}

Rules:
- Set is_calendar_request to false if this is not a request to create/schedule/add a calendar event.
- Resolve relative dates such as tomorrow from the current datetime above.
- If the user gives a start time but no duration/end time, use one hour.
- Do not invent a start time if none is supplied; set start_datetime and end_datetime to null.
- Do not execute anything and do not add commentary outside the JSON.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        proposal = json.loads(response.text)
    except (json.JSONDecodeError, ClientError, ServerError) as error:
        return {"status": "error", "message": f"Could not parse calendar request: {error}"}

    if not proposal.get("is_calendar_request"):
        return {"status": "not_calendar"}

    if not proposal.get("start_datetime") or not proposal.get("end_datetime"):
        return {
            "status": "missing_details",
            "message": "Please include the event date and start time.",
        }

    proposal["status"] = "ready"
    return proposal
