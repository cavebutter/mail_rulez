import os
import functions as pf
import process_inbox as pi
from functions import Account
import configparser
from apscheduler.schedulers.blocking import BlockingScheduler

if __name__ == "__main__":
    if os.path.isfile('./config.ini'):
        pass
    else:
        with open('.config.ini','w') as f:
            acct_name = input("Welcome to Mail-Rulez.  We are going to set up your account.\n\nPlease enter a name for your account")
            account = input("Please enter the user name for your email account:")
            password = input("Please enter the password for your email account")
            server = input("Please enter the the mailserver for your email account")
            smtp_server = input("Please enter your smtp server:")
            smtp_port = input("Please enter your smtp server port:")

            f.write(f'[{acct_name}]\naccount:{account}\npassword={password}\nserver={server}\nsmtp_server={smtp_server}\nsmtp_port={smtp_port}')

        print(f"Setting up {acct_name} and starting mail-rulez")

        ####Forwarding####
        pall_fwd_to = "cavebutter@gmail.com"
        pall_sndrs = ["postmaster@bluesombrero.com",
                      "clubnews@bluesombrero.com",
                      "chrishoglin@yahoo.com"]
        sent_mail = []
        ###################

        config = configparser.ConfigParser()
        config.read("config.ini")

        account_list = []
        for section in config.sections():
            acct = Account(config[section]["server"], config[section]["email"], config[section]["password"])
            account_list.append(acct)

        scheduler = BlockingScheduler(timezone="US/Pacific")
        for account in account_list:
            # Forwarding rules
            scheduler.add_job(lambda: pf.forward(account, pall_sndrs, pall_fwd_to, sent_mail), "interval", minutes=1)
            #  TODO some other way than hard-coding list locations
            #  TODO change this to location in docker fs
            #  Inbox
            scheduler.add_job(lambda: pi.process_inbox_maint(account), "interval", minutes=4)
            #  Approved
            scheduler.add_job(
                lambda: pf.process_folder("/home/sally/mail-rulez/lists/white.txt", account, "INBOX._Approved",
                                          "INBOX"), "interval", minutes=4)
            #  Junk
            scheduler.add_job(
                lambda: pf.process_folder("/home/sally/mail-rulez/lists/black.txt", account, "INBOX._Rejected",
                                          "INBOX.Junk"), "interval", minutes=4)
            #  Vendor
            scheduler.add_job(
                lambda: pf.process_folder("/home/sally/mail-rulez/lists/vendor.txt", account, "INBOX._Vendor",
                                          "INBOX.Approved_Ads"), "interval", minutes=4)
            #  Head
            scheduler.add_job(lambda: pf.process_folder("/home/sally/mail-rulez/lists/head.txt", account, "INBOX._HH",
                                                        "INBOX.HeadHunt"), "interval", minutes=4)

        scheduler.start()
