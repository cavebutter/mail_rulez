from imap_tools import MailBox, AND, errors
from dotenv import load_dotenv
import os

###################################################################
#                  WHAT HAPPENS IN THIS MODULE                    #
#                                                                 #
#  Fetches specified number of emails  from Pending and compares  #
#  sender to various lists.  If sender matches an entry on a list #
#  the message is moved to the appropriate folder.  If it does not#
#  match, the message is moved to Pending folder for manual dispo-#
#  sition.  This is a refresh for the pending folder so that not  #
#  all items have to be moved manually out of pending for dispo   #
#                                                                 #
###################################################################


#  TODO build log from return function
#  TODO Make an easier configuration option for limit in fetch

def process_inbox(server, account, password, folder):
    whitelisted = []
    blacklisted = []
    pending = []
    log = {}
    with open("lists/white.txt", "r") as f:
        whitelist = f.read().split("\n")
    with open("lists/black.txt", "r") as f:
        blacklist = f.read().split("\n")
    with open("lists/vendor.txt", "r") as f:
        vendorlist = f.read().split("\n")
    mb = MailBox(server).login(account, password, initial_folder=folder)
    batch = mb.fetch(limit=100, mark_seen=False, bulk=True)
    emails = {msg.uid:msg.from_ for msg in batch}
    email_list = list(emails.items())
    for item in email_list:
        if item[1] in whitelist:
            whitelisted.append(item[0])
            mb.move(whitelisted,"INBOX.Approved")
            log["Approved"] = len(whitelisted)
        elif item[1] in blacklist:
            blacklisted.append(item[0])
            mb.move(blacklisted, "INBOX.Junk")
            log["Junk"] = len(blacklisted)
        elif item[1] in vendorlist:
            blacklisted.append(item[0])
            mb.move(blacklisted, "INBOX.Approved_Ads")
            log["Vendor"] = len(blacklisted)

    return log


if __name__ == "__main__":
    #  Variables
    load_dotenv()
    server = os.getenv("server")
    account = os.getenv("jayco")
    password = os.getenv("jaypass")

    inbox = process_inbox(server, account, password, "INBOX.Pending")

    print(inbox)
