import smtplib, getpass
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from database.models import Configuration

def send_email(destination, subject, text, files=[], parts=[], attachments=[], mime_type='plain'):
    success = False
    conf = Configuration.objects.all()
    if not conf:
        print "No configuration found"
        return success
    conf = conf[0]
    gmail_user = conf.sender_email
    gmail_pwd = conf.password
    FROM = conf.sender_email
    TO = [destination]
    # message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    # """ % (FROM, ", ".join(TO), subject, text)
    # message = MIMEMultipart(
    #     From=FROM,
    #     To=TO,
    #     Subject=subject
    # )
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = FROM
    message['To'] = ', '.join(TO)

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
