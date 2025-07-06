from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os.path
import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_latest_email():
    creds = None
    # Check if token.json already exists (reuse auth)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    result = service.users().messages().list(userId='me', maxResults=1).execute()
    messages = result.get('messages', [])

    if not messages:
        print("No emails found.")
        return None, None

    msg = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
    headers = msg['payload']['headers']
    subject = next(h['value'] for h in headers if h['name'] == 'Subject')

    parts = msg['payload'].get('parts', [])
    body = ""
    for part in parts:
        if part['mimeType'] == 'text/plain':
            data = part['body']['data']
            body = base64.urlsafe_b64decode(data).decode('utf-8')
            break

    print(f"\n📬 Subject: {subject}\n")
    print(f"📄 Body: {body[:500]}...\n")
    return subject, body

from summarize_email import summarize_email
from speak import speak

subject, body = get_latest_email()
if subject and body:
    summary = summarize_email(subject, body)
    speak(summary)
