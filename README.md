# Google Calendar Events Manager
A Python application that interacts with the Google Calendar API to manage events. This program can fetch, delete, and log events from your Google Calendar, specifically targeting events that start with a specified prefix.
This is specifically useful for mass deleting events. 

## Features
- Authenticate with Google Calendar using OAuth 2.0.
- Fetch events for the next year.
- Delete events that start with a specified prefix (e.g., "CS" for the event "CS50 Intro").
- Output event details and deletion logs to a text file.

## Prerequisites
- Python 3.x
- Google Cloud Project with Calendar API enabled
- `credentials.json` file for OAuth 2.0

## Installation
1. Fork and clone the repository:
   ```bash
   git clone https://github.com/<YOUR-USERNAME>/google-calendar-events-manager.git
   cd google-calendar-events-manager
   ```
2. Install the required Python packages
    ```bash
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```
3. Enable the Google Calendar API:
    - Go to the Google Cloud Console
    - Create a new project or use an existing one
    - Enable the Google Calendar API
    - Create OAuth 2.0 credentials (as a desktop app) and download the `credentials.json` file.

## Usage
1. Run the program `python main.py`
2. Follow the prompts to authenticate your Google account and allow access to your calendar.
3. The program will fetch events from your calendar, and if any events start with the specified prefix, they will be deleted. All actions will be logged in `output.txt`.

## Licence
This prokect is licensed under the MIT License - see the LICESE file for details

## Contributing
Feel free to contribute by creating a pull request or opening an issue.

Let me know about any questions or feedback
