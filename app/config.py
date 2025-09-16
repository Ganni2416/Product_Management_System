# app/config.py
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ✅ Gmail SMTP settings
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # ✅ Gmail credentials
    MAIL_USERNAME = "jayanthg533@gmail.com"
    MAIL_PASSWORD = "bczsgwtmlcoixppi"   # App password

    # ✅ Sender email
    MAIL_DEFAULT_SENDER = "jayanthg533@gmail.com"
