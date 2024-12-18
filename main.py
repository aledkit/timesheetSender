import smtplib
import ssl
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465

def generate_body():
    """

    :return:
    """
    return 'Placeholder'

def get_secrets():
    """

    :return: dict of secrets (sender_email, sender_password, recipient_email)
    """
    with open('secrets.json') as secrets:
        s = json.load(secrets)
        return s

def main():
    """

    :return:
    """
    secrets = get_secrets()
    sender_email = secrets['sender_email']
    password = secrets['sender_password']
    receiver_email = secrets['recipient_email']

    context = ssl.create_default_context()

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'Timesheet'

    body = generate_body()
    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

if __name__ == '__main__':
    main()