
import smtplib
from email.message import EmailMessage

server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
server.ehlo()
server.starttls()
server.ehlo()

server.login("preciousemailer@yahoo.com", "uzwnfwabytncppng")
subject = "Transaction is being processed"
body = "Your order has been accepted, and is now being processed by our systems. Please check back for a confirmation email once item is shipped. Thank you!"
msg = f'Subject: {subject} \n\n{body}'
server.sendmail("preciousemailer@yahoo.com",
                "Jaredmbenitez@gmail.com", msg)

server.quit()
