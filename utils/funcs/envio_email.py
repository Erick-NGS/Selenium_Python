import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.email_info import sender_email, sender_password, receiver_email, email_subject, email_body, server_name, port_number, filename

def enviar_email():
    email_message = MIMEMultipart()
    email_message["From"] = sender_email
    email_message["To"] = receiver_email
    email_message["Subject"] = email_subject

    email_message.attach(MIMEText(email_body, "plain"))

    email_att = open(filename, "rb")
    part = MIMEBase("application", "octet-stream")
    part.set_payload(email_att.read())

    encoders.encode_base64(part)

    part.add_header("Content-Disposition", f"attachment; filename = {filename}",)

    email_message.attach(part)
    text = email_message.as_string()

    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(server_name, port_number, context=context)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, text)
    server.quit()