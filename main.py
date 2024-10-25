from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
from datetime import datetime, timezone

# Define the required scope to access Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_calendar():
    creds = None

    # Check if token.json already exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid credentials are available, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Run OAuth flow to generate token.json
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials to token.json for future use
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    # Build the Google Calendar API service
    service = build('calendar', 'v3', credentials=creds)
    return service

def list_events(service):
    with open('output.txt', 'w') as outputFile:
        """Lists all upcoming events."""
        calendars = service.calendarList().list().execute().get('items', [])
        now = datetime.now(timezone.utc).isoformat()

        for calendar in calendars:
            calendar_id = calendar['id']

            # Get events from the primary calendar starting from the current time
            events_result = service.events().list(
                calendarId=calendar_id, timeMin=now #, singleEvents=True
            ).execute()
            events = events_result.get('items', [])
            outputFile.write(f"Accessing Calendar: {calendar['summary']}")

            if not events:
                outputFile.write(f'No upcoming events found in calendar: {calendar["summary"]}')
                continue

            # Print event summaries and IDs for debugging
            for event in events:
                outputFile.write(event['summary'])
                # if event['summary'].startswith('ELEC'):
                #     print(f"Event: {event['summary']} ({event['id']}) in calendar {calendar['summary']}")
                outputFile.write("---")

# def delete_events(service):
#     # Set the current time in RFC3339 format for retrieving future events
#     now = datetime.now(timezone.utc).isoformat()  # Updated to use timezone-aware datetime

#     # Get events from the primary calendar starting from the current time
#     events_result = service.events().list(
#         calendarId='primary', timeMin=now, singleEvents=True
#     ).execute()
#     events = events_result.get('items', [])

#     if not events:
#         print('No upcoming events found.')
#         return

#     # Delete events that start with "ELEC"
#     for event in events:
#         if event['summary'].startswith('ELEC'):
#             print(f"Deleting event: {event['summary']} ({event['id']})")
#             service.events().delete(calendarId='primary', eventId=event['id']).execute()

def main():
    # Authenticate and build the service
    service = authenticate_google_calendar()
    # Delete specific events
    # delete_events(service)
    list_events(service)

if __name__ == '__main__':
    main()
