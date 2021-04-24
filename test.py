
import smtplib
from email.message import EmailMessage

with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login("preciousemailer.smtp@gmail.com", "Precious12345!")
    subject = "Transaction is being processed"
    body = "Your order has been accepted, and is now being processed by our systems. Please check back for a confirmation email once item is shipped. Thank you!"
    msg = f'Subject: {subject} \n\n{body}'
    smtp.sendmail("preciousemailer.smtp@gmail.com",
                  "Jaredmbenitez@gmail.com", msg)
