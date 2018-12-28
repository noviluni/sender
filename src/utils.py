import smtplib
import socket

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from conf import FROM_ADDRESS, EMAIL_PASSWORD, DEFAULT_TO_ADDRESS, SMTP_HOST, SMTP_PORT


def send_email(subject, text_message, html_message=None, to_address=DEFAULT_TO_ADDRESS):
    """
    Given a "subject", a "text_message" and optionally a "html_message" and a "to_address",
    send an e-mail through smtp.
    
    Returns True if e-mail has been sent, else returns False.
    
    Partially based on https://stackoverflow.com/questions/882712/sending-html-email-using-python
    """
    
    from_address = FROM_ADDRESS
    email_password = EMAIL_PASSWORD

    smtpserver = None

    try:
        # Connection with smtp service
        smtpserver = get_connection()
        
        try:
            # Login
            smtpserver = login(server, from_address, email_password)
        except smtplib.SMTPException as e:
            print("Incorrect authentication data or attempt blocked by Google. Error: {}".format(e)) # TODO: change to logging
            smtpserver.close()
            return False
    
    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException) as e:
        print("Error connecting to SMTP server. Error: {}".format(e))  # TODO: change to logging
        return False

    msg = generate_message(subject, from_address, to_address, text_message, html_message)

    # Send email
    return send(smtpserver, from_address, to_address, msg)

def get_connection(smtp_host=SMTP_HOST, port=SMTP_PORT):
    smtpserver = smtplib.SMTP(smtp_host, port)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo()
    print("Connection successful with SMTP server")  # TODO: change to logging
    return smtpserver
    
def login(smtpserver, user, password):
    smtpserver.login(user, password)
    
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

def send(smtpserver, from_address, to_address, message):
    """
    Given a logged SMTP server, a "from_address", a "to_address" and a "message", sends
    the message through the SMTP server.
    
    returns True if emails has been sent, else return False.
    """
    sent = False
    try:
        smtpserver.sendmail(from_address, to_address, message.as_string())
        sent = True
        print("Email has been sent")  # TODO: change to logging
    except smtplib.SMTPException as e:
        print("Email couldn't be sent. Error: {}".format(e))  # TODO: change to logging
    
    smtpserver.close()
    return sent
