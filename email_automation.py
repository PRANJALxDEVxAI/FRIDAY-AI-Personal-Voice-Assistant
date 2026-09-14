import os
import smtplib

from email.message import EmailMessage
from dotenv import load_dotenv


load_dotenv()


EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")


def send_email(
    recipient,
    subject,
    body,
    attachments=None,
    cc=None,
    bcc=None
):

    if not EMAIL_ADDRESS or not EMAIL_APP_PASSWORD:
        raise ValueError(
            "Email credentials are missing from .env"
        )

    if not recipient:
        raise ValueError(
            "Recipient email is required."
        )

    message = EmailMessage()

    message["From"] = EMAIL_ADDRESS
    message["To"] = recipient
    message["Subject"] = subject or ""

    if cc:
        if isinstance(cc, list):
            message["Cc"] = ", ".join(cc)
        else:
            message["Cc"] = str(cc)

    if bcc:
        if isinstance(bcc, list):
            message["Bcc"] = ", ".join(bcc)
        else:
            message["Bcc"] = str(bcc)

    message.set_content(body or "")

    if attachments:

        for attachment in attachments:

            if not os.path.isfile(attachment):
                raise FileNotFoundError(
                    f"Attachment not found: {attachment}"
                )

            with open(attachment, "rb") as file:
                file_data = file.read()

            message.add_attachment(
                file_data,
                maintype="application",
                subtype="octet-stream",
                filename=os.path.basename(attachment)
            )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465,
        timeout=60
    ) as smtp:

        smtp.login(
            EMAIL_ADDRESS,
            EMAIL_APP_PASSWORD
        )

        smtp.send_message(message)


def email_automation(
    recipient,
    subject,
    body,
    attachments=None,
    cc=None,
    bcc=None
):

    send_email(
        recipient,
        subject,
        body,
        attachments=attachments,
        cc=cc,
        bcc=bcc
    )

    return "Email sent successfully."