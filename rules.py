from imap_tools import MailBox
from datetime import datetime, timedelta
import functions as pf

def poker(server, account, password):

    date = datetime.now()
    today = date.date()

    # Move poker emails from inbox to Poker
    mb = MailBox(server).login(account, password, initial_folder="Inbox")
    batch = mb.fetch(mark_seen=False, bulk=True, reverse=True, headers_only=True, limit=100)

    #  Class mail
    mail_list = pf.class_mail(batch)

    mail_to_move = [item.uid for item in mail_list if item.from_ == "dealer@wrgpt.org"]
    mb.move(mail_to_move, "INBOX.Poker")

    #  Delete old messages from Poker folder
    mb = MailBox(server).login(account, password, initial_folder="Inbox.Poker")
    batch = mb.fetch(mark_seen=False, bulk=True, reverse=True, headers_only=True)
    mail_list2 = pf.class_mail(batch)
    for item in mail_list2:
        item.date = item.date.date()
    mail_to_delete = [item.uid for item in mail_list2 if today - item.date > timedelta(days=2)]
    mb.delete(mail_to_delete)
    return mail_list2

def linkedin(server, account, password):

    date = datetime.now()
    today = date.date()

    # Move poker emails from inbox to LinkedIn
    mb = MailBox(server).login(account, password, initial_folder="Inbox")
    batch = mb.fetch(mark_seen=False, bulk=True, reverse=True, headers_only=True, limit=100)

    #  Class mail
    mail_list = pf.class_mail(batch)

    mail_to_move = [item.uid for item in mail_list if "linkedin.com" in item.from_]
    mb.move(mail_to_move, "INBOX.LinkedIn")

    #  Delete old messages from LinkedIn folder
    mb = MailBox(server).login(account, password, initial_folder="Inbox.LinkedIn")
    batch = mb.fetch(mark_seen=False, bulk=True, reverse=True, headers_only=True, limit=100)
    mail_list2 = pf.class_mail(batch)
    for item in mail_list2:
        item.date = item.date.date()
    mail_to_delete = [item.uid for item in mail_list2 if today - item.date > timedelta(days=7)]
    mb.delete(mail_to_delete)
    return mail_list2

def old_ads(server, account, password):

    date = datetime.now()
    today = date.date()

    # Move poker emails from inbox to LinkedIn
    mb = MailBox(server).login(account, password, initial_folder="Inbox.Approved_Ads")
    batch = mb.fetch(mark_seen=False, bulk=True, reverse=True, headers_only=True, limit=100)
    mail_list2 = pf.class_mail(batch)
    for item in mail_list2:
        item.date = item.date.date()
    mail_to_delete = [item.uid for item in mail_list2 if today - item.date > timedelta(days=30)]
    mb.delete(mail_to_delete)
    return mail_list2

def old_heads(server, account, password):

    date = datetime.now()
    today = date.date()

    # Move poker emails from inbox to LinkedIn
    mb = MailBox(server).login(account, password, initial_folder="Inbox.HeadHunt")
    batch = mb.fetch(mark_seen=False, bulk=True, reverse=True, headers_only=True, limit=100)
    mail_list2 = pf.class_mail(batch)
    for item in mail_list2:
        item.date = item.date.date()
    mail_to_delete = [item.uid for item in mail_list2 if today - item.date > timedelta(days=30)]
    mb.delete(mail_to_delete)
    return mail_list2

rules_list = [poker, linkedin, old_ads, old_heads]