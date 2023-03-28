# notification_10.13.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import ssl

import config as config


class EmailNotifier:
    def __init__(self):
        self.from_email = config.EMAIL_FROM
        self.to_email = config.EMAIL_TO
        self.subject = config.EMAIL_SUBJECT
        self.smtp_server = config.SMTP_SERVER
        self.smtp_port = config.SMTP_PORT
        self.smtp_username = config.SMTP_USERNAME
        self.smtp_password = config.SMTP_PASSWORD
        self.ssl_context = ssl.create_default_context()

    def send_email(self, message):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = self.to_email
            msg['Subject'] = self.subject
            msg.attach(MIMEText(message, 'html'))
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=self.ssl_context)
            server.login(self.smtp_username, self.smtp_password)
            server.sendmail(self.from_email, self.to_email, msg.as_string())
            server.quit()
            print("Email sent successfully.")
        except Exception as e:
            print("Error sending email: ", e)
