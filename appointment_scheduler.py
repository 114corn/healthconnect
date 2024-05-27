import os
from datetime import datetime
from dotenv import load_dotenv
import requests

load_dotenv()

GOOGLE_CALENDAR_API_KEY = os.environ.get("GOOGLE_CALENDAR_API_KEY")
CALENDAR_ID = os.environ.get("CALENDAR_ID")

def authenticate_google_calendar():
    headers = {"Authorization": f"Bearer {GOOGLE_CALENDAR_API_KEY}"}
    return headers

def schedule_appointment(summary, start_time, end_time, description=""):
    url = f"https://www.googleapis.com/calendar/v3/calendars/{CALENDAR_ID}/events"
    headers = authenticate_google_calendar()
    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_time, "timeZone": "UTC"},
        "end": {"dateTime": end_time, "timeZone": "UTC"},
    }
    response = requests.post(url, headers=headers, json=event)
    if response.status_code == 200:
        return "Appointment scheduled successfully."
    else:
        return "Failed to schedule appointment."
    
def modify_appointment(event_id, summary=None, start_time=None, end_time=None, description=None):
    url = f"https://www.googleapis.com/calendar/v3/calendars/{CALENDAR_ID}/events/{event_id}"
    headers = authenticate_google_calendar()
    event = {}
    if summary:
        event["summary"] = summary
    if description:
        event["description"] = description
    if start_time:
        event["start"] = {"dateTime": start_time, "timeZone": "UTC"}
    if end_time:
        event["end"] = {"dateTime": end_time, "timeZone": "UTC"}
    
    response = requests.patch(url, headers=headers, json=event)
    if response.status_code == 200:
        return "Appointment modified successfully."
    else:
        return "Failed to modify appointment."

def cancel_appointment(event_id):
    url = f"https://www.googleapis.com/calendar/v3/calendars/{CALENDAR_ID}/events/{event_id}"
    headers = authenticate_google_calendar()
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        return "Appointment cancelled successfully."
    else:
        return "Failed to cancel appointment."

if __name__ == "__main__":
    print(schedule_appointment("Doctor's Appointment", datetime.now().isoformat(), (datetime.now() + timedelta(hours=1)).isoformat(), "General Checkup"))
    print(modify_appointment("event_id", summary="Dentist Appointment"))
    print(cancel_appointment("event_id"))