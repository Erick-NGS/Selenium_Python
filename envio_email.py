import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = "engs.3003@gmail.com"
sender_password = "mjpo zgva zimg jdlh"
receiver_email = "engs.3003@gmail.com"
email_subject = "Report de orçamento para montagem de PC"
email_body = "Olá!\n\nSegue anexo o arquivo com o orçamento pedido!\n\nAtenciosamente, Python_Bot1"
server_name = "smtp.gmail.com"
port_number = 465
filename = "Report_teste.xlsx"

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