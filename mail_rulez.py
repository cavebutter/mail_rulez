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
scheduler.add_job(lambda: pf.process_inbox(server,account,password), "interval", minutes=10)
#  Approved
scheduler.add_job(lambda: pf.process_folder("lists/white.txt",server,account,password,"INBOX._Approved", "INBOX.Processed"), "interval", minutes=8)
#  Junk
scheduler.add_job(lambda: pf.process_folder("lists/black.txt",server,account,password,"INBOX._Rejected", "INBOX.Junk"), "interval", minutes=8)
#  Vendor
scheduler.add_job(lambda: pf.process_folder("lists/vendor.txt",server,account,password,"INBOX._Vendor", "INBOX.Approved_Ads"), "interval", minutes=8)
#  Head
scheduler.add_job(lambda: pf.process_folder("lists/head.txt",server,account,password,"INBOX._HH", "INBOX.HeadHunt"), "interval", minutes=8)

scheduler.start()