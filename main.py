import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path

# Set up OAuth scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']
value = ""

def authenticate_google_calendar():
    """Authenticates the user and returns a Google Calendar API service object."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def fetch_and_delete_events(service):
    # Open output.txt with UTF-8 encoding to support all Unicode characters
    with open('output.txt', 'w', encoding='utf-8') as output_file:
        calendars = service.calendarList().list().execute().get('items', [])
        
        # Get current time and one year from now in RFC3339 format
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        one_year_later = (datetime.datetime.utcnow() + datetime.timedelta(days=365)).isoformat() + 'Z'
        
        for calendar in calendars:
            calendar_id = calendar['id']
            output_file.write(f'\nChecking calendar: {calendar["summary"]}\n')
            
            # Fetch events within the next year, including deleted ones
            events_result = service.events().list(
                calendarId=calendar_id,
                maxResults=2500,
                showDeleted=True,      # Include deleted events in the results
                singleEvents=True,     # Expand recurring events to individual instances
                timeMin=now,           # Start time for events (now)
                timeMax=one_year_later # End time for events (one year later)
            ).execute()
            
            events = events_result.get('items', [])
            
            if not events:
                output_file.write(f'No events found in calendar: {calendar["summary"]}\n')
                continue
            
            for event in events:
                # Log each event's summary and ID
                # output_file.write(f"Event: {event.get('summary', 'No Title')} (ID: {event['id']})\n")
                
                # Check if event summary starts with 'ELEC'
                if event.get('summary', '').startswith(value):
                    output_file.write(f"Deleting event: {event['summary']} (ID: {event['id']}) in calendar {calendar['summary']}\n")
                    service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()



def main():
    value = input("Enter the event starting key: ")
    service = authenticate_google_calendar()
    fetch_and_delete_events(service)

if __name__ == '__main__':
    main()