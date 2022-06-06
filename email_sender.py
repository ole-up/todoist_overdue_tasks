import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(html_file, sender, receiver, subject, smtp_server, smtp_port, smtp_password):
    """Send html file to email"""
    message = MIMEMultipart("alternative")
    with open(html_file, 'r', encoding='utf-8') as f:
        html_message = f.read()
    mime_message = MIMEText(html_message, "html")
    message.attach(mime_message)
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = receiver
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(sender, smtp_password)
        server.sendmail(sender, receiver, message.as_string())
