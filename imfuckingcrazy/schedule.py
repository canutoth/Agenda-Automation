import os.path
import datetime as dt

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

'''
color list:

01 blue
02 green
03 purple
04 red
05 yellow
06 orange
07 turquoise
08 gray
09 bold blue
10 bold green
11 bold red

'''

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials = creds)

        event = {
            "summary": "trial - number 3",
            "location": "mia casa",
            "description": "surtos da madrugada ê lê lê",
            "colorId": 3,
            "start": {
                "dateTime": "2023-12-04T02:00:00-03:00",
                "timeZone": "America/Sao_Paulo"
            },
            "end": {
                "dateTime": "2023-12-04T04:00:00-03:00",
                "timeZone": "America/Sao_Paulo"
            },
            "recurrence": [
                "RRULE:FREQ=DAILY;COUNT=1"
            ],
            "attendees": [
                {"email": "ju.tadeu.azevedo@gmail.com"}
                
            ]

        }
        
        event = service.events().insert(calendarId = "primary", body=event).execute()

        print(f"sucess, event created! (: {event.get('htmlLink')}")
        

    except HttpError as error:
        print("error: ", error)

if __name__ == "__main__":
    main()