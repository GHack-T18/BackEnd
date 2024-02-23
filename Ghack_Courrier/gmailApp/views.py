from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from base64 import urlsafe_b64decode
from email import message_from_bytes
import html2text
from django.http import JsonResponse


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']


def get_gmail_service():
  creds = None
  flow = InstalledAppFlow.from_client_secrets_file(
          "gmailApp/credentials.json", SCOPES
      )
  creds = flow.run_local_server(port=0)
  service = build("gmail", "v1", credentials=creds)
  return service



# def test(request):
#     service = get_gmail_service(request)
    

def get_emails(request):
    try:
        # Search for emails received by the authenticated user
        service = get_gmail_service()
        result = service.users().messages().list(userId='me').execute()
        messages = result.get('messages', [])
        
        if not messages:
            return JsonResponse({"status": "success", "message": "No emails found."})
        else:
            emails_data = []
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
                message_data = msg['payload']['headers']
                
                subject = next(item['value'] for item in message_data if item['name'] == 'Subject')
                sender = next(item['value'] for item in message_data if item['name'] == 'From')
                
                # Try to find the email content within the payload
                if 'parts' in msg['payload']:
                    parts = msg['payload']['parts']
                    for part in parts:
                        if part['mimeType'] == 'text/plain':
                            data = part['body']['data']
                            break
                else:
                    data = msg['payload']['body']['data']
                
                # Decode the email content
                msg_bytes = urlsafe_b64decode(data.encode('utf-8'))
                msg_obj = message_from_bytes(msg_bytes)
                
                # Convert HTML to plain text if necessary
                if msg_obj.get_content_type() == 'text/html':
                    html_content = msg_obj.get_payload()
                    text_content = html2text.html2text(html_content)
                else:
                    text_content = msg_obj.get_payload()
                
                email_info = {
                    "sender": sender,
                    "subject": subject,
                    "message": text_content
                }
                emails_data.append(email_info)
            
            return JsonResponse({"status": "success", "emails": emails_data})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)