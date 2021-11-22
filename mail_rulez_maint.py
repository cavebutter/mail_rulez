#!/home/sally/mail-rulez/venv/bin/python
# The above shebang points to a virtualenv on sally

import functions as pf
from dotenv import load_dotenv
import os
from apscheduler.schedulers.blocking import BlockingScheduler

load_dotenv()
server = os.getenv("server")
account = os.getenv("jayco")
password = os.getenv("jaypass")

scheduler = BlockingScheduler(timezone="US/Pacific")

#  Inbox
scheduler.add_job(lambda: pf.process_inbox_maint(server,account,password), "interval", minutes=5)
#  Approved
scheduler.add_job(lambda: pf.process_folder("/home/sally/mail-rulez/lists/white.txt",server,account,password,"INBOX._Approved", "INBOX.Processed"), "interval", minutes=4)
#  Junk
scheduler.add_job(lambda: pf.process_folder("/home/sally/mail-rulez/lists/black.txt",server,account,password,"INBOX._Rejected", "INBOX.Junk"), "interval", minutes=4)
#  Vendor
scheduler.add_job(lambda: pf.process_folder("/home/sally/mail-rulez/lists/vendor.txt",server,account,password,"INBOX._Vendor", "INBOX.Approved_Ads"), "interval", minutes=4)
#  Head
scheduler.add_job(lambda: pf.process_folder("/home/sally/mail-rulez/lists/head.txt",server,account,password,"INBOX._HH", "INBOX.HeadHunt"), "interval", minutes=4)

scheduler.start()
