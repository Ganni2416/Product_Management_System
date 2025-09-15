import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_key")
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SMTP config example (use env variables in production!)
    MAIL_SERVER = "smtp.mailtrap.io"
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get("21eg505808@anurag.edu.in", " ")
    MAIL_PASSWORD = os.environ.get("au12345", " ")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = "noreply@example.com"
