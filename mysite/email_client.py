import time
import smtplib, getpass
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# from database.models import Configuration
from socket import error as socket_error

import sys

def send_email(user_email, password, destinations, subject, text, files=[], parts=[], attachments=[], mime_type='plain'):
    success = False
    # conf = Configuration.objects.all()
    # if not conf:
    #     print "No configuration found"
    #     return success
    # conf = conf[0]
    # gmail_user = conf.sender_email
    # gmail_pwd = conf.password
    # FROM = conf.sender_email
    gmail_user = user_email
    gmail_pwd = password
    FROM = user_email
    TO = destinations
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = FROM
    message['To'] = ';'.join(TO)

    message.attach(MIMEText(text.encode("utf-8"), mime_type, 'utf-8'))

    for part in parts:
        message.attach(MIMEText(part["content"].encode("utf-8"), part["type"], 'utf-8'))

    for attachment in attachments:
        attach_file=MIMEApplication(attachment["content"])
        attach_file.add_header('Content-Disposition', 'attachment', filename=attachment["filename"])
        message.attach(attach_file)

    for f in files or []:
        with open(f, "rb") as fil:
            attach_file=MIMEApplication(fil.read())
            attach_file.add_header('Content-Disposition', 'attachment', filename=basename(f))
            message.attach(attach_file)

    retries = 0
    err = None
    while not success and not err and retries < 10:
        try:
            print("Sending email. Attempt: {}".format(retries+1))
            # server = smtplib.SMTP("smtp.gmail.com", 587, timeout=3)
            #server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server = smtplib.SMTP("mail.muellesobrero.com", 587, timeout=900)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            # server.sendmail(FROM, TO, message.encode('ascii', 'ignore'))
            server.sendmail(FROM, TO, message.as_string())
            server.close()
            success = True
            print('Successfully sent the mail')
        except socket_error as e:
            retries += 1
            if retries == 10:
                print("Failed to send mail")
                print(e)
                err = e
            else:
                time.sleep(7)
        except Exception as e:
            print("Failed to send mail")
            print(e)
            err = e
    return success
