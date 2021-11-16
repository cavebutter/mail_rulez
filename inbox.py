from imap_tools import MailBox, AND, errors
from dotenv import load_dotenv
import os


def process_inbox(server, account, password, folder):
    whitelisted = []
    blacklisted = []
    pending = []
    log = {}
    with open("white.txt", "r") as f:
        whitelist = f.read().split("\n")
    with open("black.txt","r") as f:
        blacklist = f.read().split("\n")
    mb = MailBox(server).login(account, password, initial_folder=folder)
    batch = mb.fetch(limit=25, mark_seen=False, bulk=True)
    emails = {msg.uid:msg.from_ for msg in batch}
    email_list = list(emails.items())
    for item in email_list:
        if item[1] in whitelist:
            whitelisted.append(item[0])
            mb.move(whitelisted,"INBOX.Approved")
            log["Approved"] = len(whitelisted)
        elif item[1] in blacklist:
            blacklisted.append(item[0])
            mb.move(blacklisted, "Junk")
            log["Junk"] = len(blacklisted)
        else:
            pending.append(item[0])
            mb.move(pending, "INBOX.Pending")
            log["Pending"] = len(pending)

    return log


if __name__ == "__main__":
    #  Variables
    load_dotenv()
    server = os.getenv("server")
    account = os.getenv("jayco")
    password = os.getenv("jaypass")

    email_list = process_inbox(server, account, password, "INBOX")

    print(email_list)
