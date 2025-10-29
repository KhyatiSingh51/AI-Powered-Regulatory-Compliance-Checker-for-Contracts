import smtplib
from email.mime.text import MIMEText

#first we will add email part


def send_notification(subject, notification):

    
      # Email details
    try:
        sender = "23cs3033@rgipt.ac.in"
        password = "wccm ykaf jvzh gycw"
        receiver = "khyatisingh.smn@gmail.com"



         # Create message
        msg = MIMEText(f"{notification}")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver
        # Connect to Gmail SMTP server


        with smtplib.SMTP("smtp.gmail.com", 587) as server:
          server.starttls()  # Start TLS encryption
          server.login(sender, password)
          server.send_message(msg)

        print("Email sent successfully!")

    except Exception as e:
       print("Error Occured", e)
