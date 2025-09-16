# app/emailer.py

import smtplib
from email.message import EmailMessage
import threading
from flask import current_app

def send_email(subject: str, body: str, to: str):
    app = current_app._get_current_object()
    with app.app_context():  # ✅ Push app context inside thread
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
                app.logger.info(f"✅ Email sent to {to}")
        except Exception as e:
            app.logger.error(f"❌ Failed to send email: {e}")

def send_email_async(subject: str, body: str, to: str):
    # ✅ Capture current app to use it inside thread
    app = current_app._get_current_object()
    thread = threading.Thread(target=lambda: send_email_with_context(app, subject, body, to))
    thread.daemon = True
    thread.start()

def send_email_with_context(app, subject, body, to):
    with app.app_context():
        send_email(subject, body, to)
