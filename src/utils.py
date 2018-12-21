import smtplib
import socket

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from conf import GMAIL_USER, GMAIL_PASSWORD, DEFAULT_TO_ADDRESS


def send_email(subject, text_message, html_message=None, to_address=DEFAULT_TO_ADDRESS, **kwargs):
    # Partially based on https://stackoverflow.com/questions/882712/sending-html-email-using-python

    try:
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        print("Conexion exitosa con Gmail")  # TODO: change to logging

        try:
            gmail_user = GMAIL_USER
            gmail_pwd = GMAIL_PASSWORD
            smtpserver.login(gmail_user, gmail_pwd)

        except smtplib.SMTPException as e:
            print("Autenticacion incorrecta o intento bloqueado por parte de Google. Error: {}".format(e))
            # TODO: change to logging
            smtpserver.close()
            return False

    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException) as e:
        print("Fallo en la conexion con Gmail. Error: {}".format(e))  # TODO: change to logging
        return False

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = to_address

    part1 = MIMEText(text_message, 'plain')
    msg.attach(part1)

    if html_message:
        part2 = MIMEText(html_message, 'html')
        msg.attach(part2)

    try:
        smtpserver.sendmail(gmail_user, to_address, msg.as_string())
        print("El correo se envio correctamente")  # TODO: change to logging
        smtpserver.close()
        return True

    except smtplib.SMTPException as e:
        print("El correo no pudo ser enviado. Error: {}".format(e))  # TODO: change to logging
        smtpserver.close()
        return False
