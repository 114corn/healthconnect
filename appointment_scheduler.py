import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests

load_dotenv()

GOOGLE_CALENDAR_API_KEY = os.environ.get("GOOGLE_CALENDAR_API_KEY")
CALENDAR_ID = os.environ.get("CALENDAR_ID")

def authenticate_google_calendar():
    headers = {"Authorization": f"Bearer {GOOGLE_CALENDAR_API_KEY}"}
    return headers

def create_event_data(summary, start_time, end_time, description=""):
    """Helper function to create event data structure."""
    return {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_time, "timeZone": "UTC"},
        "end": {"dateTime": end_time, "timeZone": "UTC"},
    }

def post_event(url, headers, event):
    """Helper function to post event to Google Calendar."""
    response = requests.post(url, headers=headers, json=event)
    return response.json(), response.status_code

def patch_event(url, headers, event):
    """Helper function to patch (update) an event on Google Calendar."""
    response = requests.patch(url, headers=headers, json=event)
    return response.json(), response.status_code

def delete_event(url, headers):
    """Helper function to delete an event from Google Calendar."""
    response = requests.delete(url, headers=headers)
    return response.status_code

def schedule_appointment(summary, start_time, end_time, description=""):
    url = f"https://www.googleapis.com/calendar/v3/calendars/{CALENDAR_ID}/events"
    headers = authenticate_google_calendar()
    event = create_event_data(summary, start_time, end_time, description)
    response_json, status_code = post_event(url, headers, event)
    if status_code == 200:
        return "Appointment scheduled successfully."
    else:
        return f"Failed to schedule appointment. Error: {response_json.get('error', {}).get('message', 'Unknown error')}"

def modify_appointment(event_id, summary=None, start_time=None, end_time=None, description=None):
    url = f"https://www.googleapis.com/calendar/v3/calendars/{CALENDAR_ID}/events/{event_id}"
    headers = authenticate_google_calendar()
    event = create_event_data(summary if summary else "", start_time if start_time else "", end_time if end_time else "", description if description else "")
    response_json, status_code = patch_event(url, headers, event)
    if status_code == 200:
        return "Appointment modified successfully."
    else:
        return f"Failed to modify appointment. Error: {response_json.get('error', {}).get('message', 'Unknown error')}"

def cancel_appointment(event_id):
    url = f"https://www.googleapis.com/calendar/v3/calendars/{CALENDAR_ID}/events/{event_id}"
    headers = authenticate_google_calendar()
    status_code = delete_event(url, headers)
    if status_code == 204:
        return "Appointment cancelled successfully."
    else:
        return "Failed to cancel appointment."

def list_appointments(min_time, max_time):
    """Function to list all events in a specified time range."""
    url = f"https://www.googleapis.com/calendar/v3/calendars/{CALENDAR_ID}/events?timeMin={min_time}&timeMax={max_time}&orderBy=startTime&singleEvents=true"
    headers = authenticate_google_calendar()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        events = response.json().get('items', [])
        if not events:
            return "No appointments found."
        appointments = []
        for event in events:
            appointments.append({
                'id': event['id'],
                'summary': event['summary'],
                'start': event['start']['dateTime'],
                'end': event['end']['dateTime'],
                'description': event.get('description', '')
            })
        return appointments
    else:
        return f"Failed to list appointments. Error: {response.json().get('error', {}).get('message', 'Unknown error')}"

if __name__ == "__main__":
    now = datetime.now().isoformat() + 'Z'  # Z indicates UTC time
    future = (datetime.now() + timedelta(days=7)).isoformat() + 'Z'
    print(schedule_appointment("Doctor's Appointment", now, (datetime.now() + timedelta(hours=1)).isoformat(), "General Checkup"))
    print(list_appointments(now, future))