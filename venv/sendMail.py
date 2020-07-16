import smtplib
from email.mime.text import MIMEText
#Take out privateInfo and input your own private information
import privateInfo
mailFrom = privateInfo.amazonUsername
mailTo = [privateInfo.botUsername]
smtp_ssl_host = 'smtp-pulse.com'
smtp_ssl_port = 587
#email username
username = privateInfo.botUsername
password = privateInfo.botPassword

class sendM:
    mailSubject = 'Amazon Items'
    def __init__(self,message):
        self.message = message
    def sending(self):
        message = MIMEText(self.message)
        message['subject'] = 'Amazon Item Bot'
        message['from'] = mailFrom
        message['to'] = ', '.join(mailTo)


        message = 'Subject: {}\n\n{}'.format('Amazon Item Bot - OPEN',self.message)
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username,password)
        server.sendmail(username,username,message)
        server.quit()


