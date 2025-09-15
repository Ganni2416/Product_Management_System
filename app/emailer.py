# app/emailer.py
import smtplib
from email.message import EmailMessage
import threading
from flask import current_app

def send_email(subject: str, body: str, to: str):
    """Send an email using SMTP configured in Flask app config."""
    app = current_app._get_current_object()
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = app.config["MAIL_DEFAULT_SENDER"]
    msg["To"] = to
    msg.set_content(body)

    try:
        with smtplib.SMTP(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]) as server:
            server.starttls()
            server.login(app.config["MAIL_USERNAME"], app.config["MAIL_PASSWORD"])
            server.send_message(msg)
    except Exception as e:
        app.logger.error(f"Failed to send email: {e}")

def send_email_async(subject: str, body: str, to: str):
    """Run send_email in a separate thread."""
    thread = threading.Thread(target=send_email, args=(subject, body, to))
    thread.daemon = True
    thread.start()
