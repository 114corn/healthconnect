import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests

load_dotenv()

GOOGLE_CALENDAR_API_KEY = os.environ.get("GOOGLE_CALENDAR_API_KEY")
CALENDAR_ID = os.environ.get("CALENDAR_ID")

def get_authentication_headers():
    return {"Authorization": f"Bearer {GOOGLE_CALENDAR_API_KEY}"}

def construct_event_data(summary, start_time, end_time, description=""):
    return {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_time, "timeZone": "UTC"},
        "end": {"dateTime": end_time, "timeZone": "UTC"},
    }

def post_event_to_calendar(url, headers, event):
    response = requests.post(url, headers=headers, json=event)
    return response.json(), response.status_code

def update_calendar_event(url, headers, event):
    response = requests.patch(url, headers=headers, json=event)
    return response.json(), response.status_code

def remove_event_from_calendar(url, headers):
    response = requests.delete(url, headers=headers)
    return response.status_code

def schedule_appointment(summary, start_time, end_time, description=""):
    url = f"https://www.googleapis.com/calendar/v3/calendars/{CALENDAR_ID}/events"
    headers = get_authentication_headers()
    event = construct_event_data(summary, start_time, end_time, description)
    response_json, status_code = post_event_to_calendar(url, headers, event)
    if status_code == 200:
        return "Appointment scheduled successfully."
    return f"Failed to schedule appointment. Error: {response_json.get('error', {}).get('message', 'Unknown error')}"

def modify_appointment(event_id, summary=None, start_time=None, end_time=None, description=None):
    url = f"https://www.googleapis.com/calendar/v3/calendars/{CALENDAR_ID}/events/{event_id}"
    headers = get_authentication_headers()
    event = construct_event_data(summary or "", start_time or "", end_time or "", description or "")
    response_json, status_code = update_calendar_event(url, headers, event)
    if status_code == 200:
        return "Appointment modified successfully."
    return f"Failed to modify appointment. Error: {response_json.get('error', {}).get('message', 'Unknown error')}"

def cancel_appointment(event_id):
    url = f"https://www.googleapis.com/calendar/v3/calendars/{CALENDAR_ID}/events/{event_id}"
    headers = get_authentication_headers()
    status_code = remove_event_from_calendar(url, headers)
    if status_code == 204:
        return "Appointment cancelled successfully."
    return "Failed to cancel appointment."

def list_appointments(min_time, max_time):
    url = (f"https://www.googleapis.com/calendar/v3/calendars/{CALENDAR_ID}/"
           f"events?timeMin={min_time}&timeMax={max_time}&orderBy=startTime&singleEvents=true")
    headers = get_authentication_headers()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        events = response.json().get('items', [])
        if not events:
            return "No appointments found."
        return [{'id': e['id'], 'summary': e['summary'], 'start': e['start']['dateTime'], 'end': e['end']['dateTime'], 'description': e.get('description', '')} for e in events]
    return f"Failed to list appointments. Error: {response.json().get('error', {}).get('je', 'Unknown error')}"

if __name__ == "__main__":
    now = datetime.now().isoformat() + 'Z'
    future = (datetime.now() + timedelta(days=7)).isoformat() + 'Z'
    print(schedule_appointment("Doctor's Appointment", now, (datetime.now() + timedelta(hours=1)).isoformat(), "General Checkup"))
    print(list_appointments(now, future))