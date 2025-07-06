import base64
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def read_latest_email():
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        # If there are no (valid) credentials, let the user log in.
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(userId='me', maxResults=1).execute()
    messages = results.get('messages', [])

    if not messages:
        return pd.DataFrame([{"Subject": "No Mail", "Body": "You don't have any emails."}])

    msg = service.users().messages().get(userId='me', id=messages[0]['id']).execute()

    headers = msg['payload']['headers']
    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")

    parts = msg['payload'].get('parts', [])
    body = ""

    if parts:
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
                body = base64.urlsafe_b64decode(data).decode('utf-8')
                break
    else:
        # Handle non-multipart emails
        if msg['payload']['mimeType'] == 'text/plain':
            data = msg['payload']['body'].get('data')
            if data:
                body = base64.urlsafe_b64decode(data).decode('utf-8')

    df = pd.DataFrame([{"Subject": subject, "Body": body}])
    return df
