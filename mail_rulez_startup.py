#!/home/sally/mail-rulez/venv/bin/python
# The above shebang points to a virtualenv on sally

import functions as pf
import process_inbox as pi
from functions import Account
import configparser
from apscheduler.schedulers.blocking import BlockingScheduler

config = configparser.ConfigParser()
config.read("config.ini")

account_list = []
for section in config.sections():
    acct = Account(config[section]["server"],config[section]["email"], config[section]["password"])
    account_list.append(acct)



scheduler = BlockingScheduler(timezone="US/Pacific")
for account in account_list:
#  TODO some other way than hard-coding list locations
    #  Inbox
    scheduler.add_job(lambda: pi.process_inbox(account), "interval", minutes=5)
    #  Approved
    scheduler.add_job(lambda: pf.process_folder("/home/sally/mail-rulez/lists/white.txt", account,"INBOX._Approved", "INBOX"), "interval", minutes=4)
    #  Junk
    scheduler.add_job(lambda: pf.process_folder("/home/sally/mail-rulez/lists/black.txt", account,"INBOX._Rejected", "INBOX.Junk"), "interval", minutes=4)
    #  Vendor
    scheduler.add_job(lambda: pf.process_folder("/home/sally/mail-rulez/lists/vendor.txt", account,"INBOX._Vendor", "INBOX.Approved_Ads"), "interval", minutes=4)
    #  Head
    scheduler.add_job(lambda: pf.process_folder("/home/sally/mail-rulez/lists/head.txt", account,"INBOX._HH", "INBOX.HeadHunt"), "interval", minutes=4)

scheduler.start()
