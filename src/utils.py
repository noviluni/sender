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
        print("Conexion exitosa con Gmail")  # TODO: change to loggin

        try:
            gmail_user = GMAIL_USER
            gmail_pwd = GMAIL_PASSWORD
            smtpserver.login(gmail_user, gmail_pwd)

        except smtplib.SMTPException as e:
            print("Autenticacion incorrecta o intento bloqueado por parte de Google. Error: {}".format(e))  # TODO: change to loggin
            smtpserver.close()
            return False

    except (socket.gaierror, socket.error, socket.herror, smtplib.SMTPException) as e:
        print("Fallo en la conexion con Gmail. Error: {}".format(e))  # TODO: change to loggin
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
        print("El correo se envio correctamente")  # TODO: change to loggin
        smtpserver.close()
        return True

    except smtplib.SMTPException as e:
        print("El correo no pudo ser enviado. Error: {}".format(e))  # TODO: change to loggin
        smtpserver.close()
        return False


# if __name__ == '__main__':
#     subject = "Movimientos en tus cuentas"
#     body_text = "Movimientos!!"
#
#     try:
#         f = codecs.open("templates/prueba.html", 'r', 'utf-8')
#         body_html = f.read()
#         f.close()
#     except FileNotFoundError as e:
#         print("No existe la platilla html")
#         body_html = body_text
#
#     send_email(subject, body_text, body_html=None, to_email='noviluni@gmail.com')
