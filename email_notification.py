import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import List, Dict, Any
import sqlite3

class EmailNotification:
    def __init__(self, db_path: str):
        """
        Initializes the EmailNotification class.

        Args:
            db_path (str): The path to the SQLite database file.
        """
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def __del__(self):
        """
        Closes the connection to the database when the object is deleted.
        """
        self.conn.close()

    def send_email(self, recipient: str, subject: str, body: str, attachments: List[Dict[str, Any]] = []) -> None:
        """
        Sends an email to the specified recipient with the given subject and body.

        Args:
            recipient (str): The email address of the recipient.
            subject (str): The subject of the email.
            body (str): The body of the email.
            attachments (List[Dict[str, Any]]): A list of dictionaries representing attachments, with keys "filename" and "content".
        """
        # Get email settings from the database
        self.cursor.execute("SELECT * FROM email_settings")
        settings = self.cursor.fetchone()

        # Create the message
        message = MIMEMultipart()
        message["From"] = settings[0]
        message["To"] = recipient
        message["Subject"] = subject
        message.attach(MIMEText(body))

        # Add attachments
        for attachment in attachments:
            with open(attachment["filename"], "rb") as f:
                attachment_data = f.read()
            part = MIMEApplication(attachment_data, Name=attachment["filename"])
            part["Content-Disposition"] = f'attachment; filename="{attachment["filename"]}"'
            message.attach(part)

        # Send the email
        with smtplib.SMTP(settings[1], settings[2]) as server:
            server.login(settings[3], settings[4])
            server.sendmail(settings[0], recipient, message.as_string())
