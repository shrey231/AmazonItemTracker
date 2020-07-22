import imaplib
import base64
import os
import email
#Take out privateInfo and input your own private information
import privateInfo
emailAdd = privateInfo.botUsername
password = privateInfo.botPassword
server = 'imap.gmail.com'
class receiveM:
    def receive(self):
        mail = imaplib.IMAP4_SSL(server,993)
        mail.login(emailAdd, password)
        mail.select('inbox')

        search_criteria = 'REVERSE DATE'
        #mail.sort(search_criteria,'UTF-8','ALL')

        result, data = mail.uid('search',None,"ALL")
        inbox_item = data[0].split()
        recent = inbox_item[-1]
        result2, email_data = mail.uid('fetch', recent, '(RFC822)')
        raw = email_data[0][1].decode("utf-8")

        msg = email.message_from_string(raw)
        return msg.get_payload()