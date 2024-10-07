from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import datetime

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    """Shows basic usage of the Google Calendar API.
    Returns a service object for interacting with the Google Calendar API.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is created automatically
    # when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service

def delete_events(service):
    # Get the current time (RFC3339 format) to fetch only future events
    now = datetime.datetime.utcnow().isoformat() + 'Z'

    # Fetch all events starting with "ELEC"
    events_result = service.events().list(calendarId='primary', timeMin=now, singleEvents=True).execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return

    for event in events:
        if event['summary'].startswith('ELEC'):
            print(f"Deleting event: {event['summary']} ({event['id']})")
            service.events().delete(calendarId='primary', eventId=event['id']).execute()

def main():
    service = authenticate_google_calendar()
    delete_events(service)

if __name__ == '__main__':
    main()
