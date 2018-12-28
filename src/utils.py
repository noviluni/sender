import smtplib
import socket

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from conf import GMAIL_USER, GMAIL_PASSWORD, DEFAULT_TO_ADDRESS


def send_email(subject, text_message, html_message=None, to_address=DEFAULT_TO_ADDRESS):
    """
    Given a "subject", a "text_message" and optionally a "html_message" and a "to_address",
    send an e-mail through gmail smtp.
    
    Returns True if e-mail has been sent, else returns False.
    
    Partially based on https://stackoverflow.com/questions/882712/sending-html-email-using-python
    """
    

    try:
        # Connection with gmail
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        print("Connection successful with Gmail")  # TODO: change to logging

        # Login
        try:
            smtpserver.login(gmail_user, gmail_pwd)

        except smtplib.SMTPException as e:
            print("Incorrect authentication data or attempt blocked by Google
            Autenticacion incorrecta o intento bloqueado por parte de Google. Error: {}".format(e))
            # TODO: change to logging
            smtpserver.close()
            return False

    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException) as e:
        print("Error connecting to Gmail. Error: {}".format(e))  # TODO: change to logging
        return False

    msg = generate_message(subject, gmail_user, to_address, text_message, html_message)

    # Send email
    try:
        smtpserver.sendmail(gmail_user, to_address, msg.as_string())
        print("Email has be sent")  # TODO: change to logging
        smtpserver.close()
        return True

    except smtplib.SMTPException as e:
        print("Email couldn't be sent. Error: {}".format(e))  # TODO: change to logging
        smtpserver.close()
        return False
    
    
    def generate_message(subject, from_address, to_address, text_message, html_message):
        """
        Generates an email (MIMEMultipart object) to be sended.
        """ 
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_address
        msg['To'] = to_address
        part1 = MIMEText(text_message, 'plain')
        msg.attach(part1)

        if html_message:
            part2 = MIMEText(html_message, 'html')
            msg.attach(part2)
        return msg
