import datetime as dt
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def google_handler(gpt_response, username):

  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(f"tokens/{username}token.json"):
    creds = Credentials.from_authorized_user_file(f"tokens/{username}token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:  
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(f"tokens/{username}token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)
    
    event = {
        "summary": gpt_response['summary'],
        "location": gpt_response['location'],
        "colorId": 6,
        "start": {
            "dateTime": gpt_response['start_dateTime'],
            "timeZone": "Asia/Singapore"
        },
        "end": {
            "dateTime": gpt_response['end_dateTime'],
            "timeZone": "Asia/Singapore"
        },
        
    }
    
    event = service.events().insert(calendarId="primary", body=event).execute()
    
    print(f"Event created {event.get('htmlLink')}")
    
  except HttpError as error:
    print(f"An error occurred: {error}")
    


def connect_to_google(username):
  creds = None
  if os.path.exists(f"tokens/{username}token.json"):
    creds = Credentials.from_authorized_user_file(f"tokens/{username}token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:  
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(f"tokens/{username}token.json", "w") as token:
      token.write(creds.to_json())


# if __name__ == "__main__":
#   main()