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
    return response

def patch_event(url, headers, event):
    """Helper function to patch (update) an event on Google Calendar."""
    response = requests.patch(url, headers=headers, json=event)
    return response

def delete_event(url, headers):
    """Helper function to delete an event from Google Calendar."""
    response = requests.delete(url, headers=headers)
    return response

def schedule_appointment(summary, start_time, end_time, description=""):
    url = f"https://www.googleapis.com/calendar/v3/calendars/{CALENDAR_ID}/events"
    headers = authenticate_google_calendar()
    event = create_event_data(summary, start_time, end_time, description)
    response = post_event(url, headers, event)
    if response.status_code == 200:
        return "Appointment scheduled successfully."
    else:
        return f"Failed to schedule appointment. Error: {response.text}"

def modify_appointment(event_id, summary=None, start_time=None, end_time=None, description=None):
    url = f"https://www.googleapis.com/calendar/v3/calendars/{CALENDAR_ID}/events/{event_id}"
    headers = authenticate_google_calendar()
    event = create_event_data(summary if summary else "", start_time if start_time else "", end_time if end_time else "", description if description else "")
    response = patch_event(url, headers, event)
    if response.status_code == 200:
        return "Appointment modified successfully."
    else:
        return f"Failed to modify appointment. Error: {response.text}"

def cancel_appointment(event_id):
    url = f"https://www.googleapis.com/calendar/v3/calendars/{CALENDAR_ID}/events/{event_id}"
    headers = authenticate_google_calendar()
    response = delete_event(url, headers)
    if response.status_code == 204:
        return "Appointment cancelled successfully."
    else:
        return f"Failed to cancel appointment. Error: {response.text}"

if __name__ == "__main__":
    # Example usage
    now = datetime.now()
    print(schedule_appointment("Doctor's Appointment", now.isoformat(), (now + timedelta(hours=1)).isoformat(), "General Checkup"))
    print(modify_appointment("your_event_id_here", summary="Dentist Appointment"))
    print(cancel_appointment("your_event_id_here"))