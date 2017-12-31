import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import os
import sys

def send_email(user_email, password, destination, subject, text, files=[], parts=[], attachments=[], mime_type='plain'):
    success = False
    gmail_user = user_email
    gmail_pwd = password
    FROM = user_email
    TO = destination
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = FROM
    message['To'] = ';'.join(TO)

    message.attach(MIMEText(text.encode("utf-8"), mime_type, 'utf-8'))

    for part in parts:
        message.attach(MIMEText(part["content"].encode("utf-8"), part["type"], 'utf-8'))

    for attachment in attachments:
        attach_file=MIMEApplication(attachment["content"].encode('utf-8'))
        attach_file.add_header('Content-Disposition', 'attachment', filename=attachment["filename"])
        message.attach(attach_file)

    for f in files or []:
        with open(f, "rb") as fil:
            attach_file=MIMEApplication(fil.read())
            attach_file.add_header('Content-Disposition', 'attachment', filename=basename(f))
            message.attach(attach_file)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        #server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        # server.sendmail(FROM, TO, message.encode('ascii', 'ignore'))
        server.sendmail(FROM, TO, message.as_string())
        server.close()
        success = True
        print 'Successfully sent the mail'
    except Exception as e:
        print "Failed to send mail"
        print e
    return success

if __name__ == '__main__':
    r = requests.get('http://ipecho.net/plain')
    curr_ip = r.content
    prev_ip = ''
    if os.path.exists('/home/gbriones/public_ip'):
        with open("/home/gbriones/public_ip", "r") as f:
            prev_ip = f.read()
    if prev_ip != curr_ip:
        print("IP changed")
        with open("/home/gbriones/public_ip", "w") as f:
            f.write(r.content)
        send_email(sys.argv[1], sys.argv[2], ["gbriones.gdl@gmail.com", "mind.braker@hotmail.com"], "Cambio de direccion", curr_ip)
    else:
        print("No IP change")
