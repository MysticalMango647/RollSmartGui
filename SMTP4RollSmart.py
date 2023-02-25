import ssl
from email.message import EmailMessage
import ssl
import smtplib
#variables
email = 'sysc4907rollsmart@gmail.com'
password = 'Sysc4907'
securePassword = 'fxnoeivordwkvtkf'
receivingEmail = 'yunas.magsi@gmail.com'

# For Email Notifications

#
sub = 'New Account Created for RollSmart User'
bod = """
Welcome to RollSmart!

Your Username is your email.
Your Password is XYZ.

If you have any issues, please contact your doctors office.

-RollSmart
"""

#Set Elements of email
emailObject = EmailMessage()
emailObject['From'] = email
emailObject['To'] = receivingEmail
emailObject['Subject'] = sub
emailObject.set_content(bod)

#adding ssl security for email transmission
securityContent = ssl.create_default_context()

#Sending the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = securityContent) as smtp:
    smtp.login(email, securePassword)
    smtp.sendmail(email, receivingEmail, emailObject.as_string())

print("Email Sent")













#Ref: https://www.youtube.com/watch?v=g_j6ILT-X0k&ab_channel=ThePyCoach