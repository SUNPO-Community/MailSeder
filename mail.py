import csv
import os
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

sender_email = os.getenv("SENDER_EMAIL")
app_password = os.getenv("APP_PASSWORD")

def send_email_with_pdf(sender_email, receiver_email, subject, body, pdf_filename, smtp_server, port, login, password):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with open(pdf_filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename={pdf_filename}",
    )

    message.attach(part)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

def send_bulk_emails(receivers_pdfs, subject, body, smtp_server, port, sender_email, app_password):
    for receiver_email, pdf_filename in receivers_pdfs:
        send_email_with_pdf(sender_email, receiver_email, subject, body, pdf_filename, smtp_server, port, sender_email, app_password)
        print(f"Email sent to {receiver_email} with PDF: {pdf_filename}")


def read_list(csv_filename):
    emails = []
    with open(csv_filename, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            emails.append(row['members'])
    return emails

def send_to_admins(admin_emails, bulk_folder_path, smtp_server, port, sender_email, app_password):
    subject = "SunpoFest'24 Sertifikaları"
    body = """SUNPOFest24'e katılımınızı belirten sertifika ilişiktedir. Katılımınız için teşekkür ediyor, SUNPOFest25'te tekrar bir araya gelmeyi diliyoruz. 

SUNPO Community'nin yeni eğitim döneminde gerçekleştireceği etkinliklerden haberdar olmak için @sunpocommunity instagram hesabını takipte kalın 🙌🏻

Sevgiler,
Sunpo 💙🤍"""
    receivers_pdfs = []
    
    for idx, admin_email in enumerate(admin_emails, start=1):
        pdf_filename = f"{bulk_folder_path}/(Bulk 1) Copy of SunpoFest Sertifika (1)-{idx}.pdf"
        receivers_pdfs.append((admin_email, pdf_filename))

    send_bulk_emails(receivers_pdfs, subject, body, smtp_server, port, sender_email, app_password)

def send_to_participants(participant_emails, bulk_folder_path, smtp_server, port, sender_email, app_password):
    subject = "SunpoFest'24 Sertifikaları"
    body = """SUNPOFest24'te admin olarak yer aldığınızı belirten sertifika ilişiktedir. Konferansın içeriğini zenginleştiren, organizasyonunu kolaylaştıran ve katılımcıların keyifli vakit geçirmesini sağlayan tüm admin'lere emekleri için teşekkür ediyor, SUNPOFest25'te tekrar bir araya gelmeyi diliyoruz. 

SUNPO Community'nin yeni eğitim döneminde gerçekleştireceği etkinliklerden haberdar olmak için @sunpocommunity instagram hesabını takipte kalın 🙌🏻

Sevgiler,
Sunpo 💙🤍"""
    receivers_pdfs = []
    
    for idx, admin_email in enumerate(participant_emails, start=1):
        pdf_filename = f"{bulk_folder_path}/(Bulk 1) Copy of SunpoFest Sertifika (2)-{idx+31}.pdf"
        receivers_pdfs.append((admin_email, pdf_filename))

    send_bulk_emails(receivers_pdfs, subject, body, smtp_server, port, sender_email, app_password)

def main():
    smtp_server = "smtp.gmail.com"
    port = 465 

    admin_emails = read_list("admin_list.csv")
    participants = read_list("participants_list.csv")

    send_to_admins(admin_emails, "admin", smtp_server, port, sender_email, app_password)
    send_to_participants(participants, "participant", smtp_server, port, sender_email, app_password)

# Run the main function
if __name__ == "__main__":
    main()
