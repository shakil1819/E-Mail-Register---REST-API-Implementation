from dotenv import load_dotenv
from Google import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

def send_user_registration_email(subject, message, user_email):
    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    #emailMsg = f'Welcome to our platform, {user}!'
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = user_email
    mimeMessage['subject'] = 'Registration Confirmation Email'
    mimeMessage.attach(MIMEText(message, 'plain'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
    try:
        message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
        print("Email sent successfully:", message)
    except Exception as e:
        print("An error occurred while sending the email:", e)

# Example usage:
# send_user_registration_email('Welcome!', 'example@gmail.com', 'John Doe')
