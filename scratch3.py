import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imap_tools
from functions import Account

smtp_server = "smtp.dreamhost.com"
smtp_port = 465
account_email = "jay@jay-cohen.info"
imap_server = "imap.dreamhost.com"
forward_addr = "cavebutter@gmail.com"
password = "plasticfantastic"
addr_to_fwd = ["clubnews@bluesombrero.com"]

account = Account(imap_server,account_email,password)

login = account.login()
for msg in login.fetch():
    if msg.from_ in addr_to_fwd:
        message = f"""----------------------------------<br>
FROM:  {msg.from_}<br>
TO:  {msg.to}<br>
SUBJECT:  FWD: {msg.subject}<br><br>

{msg.html}"""

        ######  EMAIL  #######

        mail = MIMEMultipart()
        mail["Subject"] = msg.subject
        mail["From"] = account_email
        mail["To"] = forward_addr
        mail.attach(MIMEText(message, "html"))

        #  Try to connect to mailserver and send
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(account_email, password)
            server.sendmail(account_email, forward_addr, mail.as_string())