import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

email_sender = "amitojsinghmehta098@gmail.com"
email_pass = os.getenv("EMAIL_PASS")


def send_otp(receiver, otp):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_sender, email_pass)
        server.sendmail(
            email_sender,
            receiver,
            f"Subject:Your OTP for Bondly\n\nYour OTP is {otp}, Don't share it with anyone",
        )
        print("OTP sent")
