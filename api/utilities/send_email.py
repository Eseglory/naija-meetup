import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

def read_template(filename):
    with open(filename, "r") as file:
        template = file.read()
    return template

def send_email(receiver_email, subject, body):
    # Create message container
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = os.getenv("MAIL_FROM")
    msg['To'] = receiver_email
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP(os.getenv("MAIL_SERVER"), os.getenv("MAIL_PORT")) as server:
            server.starttls()
            server.login(os.getenv("MAIL_USERNAME"), os.getenv("MAIL_PASSWORD"))
            server.sendmail(os.getenv("MAIL_PORT"), receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

async def send_otp_email(receiver_email, otp, receiver_name):
    email_template = read_template("api/templates/registration_email.html")
    email_template = email_template.replace("{{OTP}}", otp).replace("{{Name}}", receiver_name)

    send_email(receiver_email, "OTP Verification", email_template)

async def send_custom_email(title, receiver_email, otp, receiver_name, message):
    email_template = read_template("api/templates/custom_email.html")
    email_template = email_template.replace("{{Title}}", title).replace("{{Name}}", receiver_name).replace("{{Message}}", message)

    send_email(receiver_email, title, email_template)
