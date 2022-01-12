from functions import Rule
import functions as pf


rule = Rule()

@rule
def poker(account):
    login = account.login()
    mail_list = pf.fetch_class(login)
    mail_to_move = [item.uid for item in mail_list if item.from_ == "dealer@wrgpt.org"]
    login.move(mail_to_move, "INBOX.Poker")

    #  Delete old messages from Poker folder
    pf.purge_old(login, folder="INBOX.Poker", age=2)

@rule
def linkedin(account):
    login = account.login()
    # Move emails from inbox to linkedin
    mail_list = pf.fetch_class(login)
    mail_to_move = [item.uid for item in mail_list if "linkedin.com" in item.from_]
    login.move(mail_to_move, "INBOX.LinkedIn")

    #  Delete old messages from LinkedIn folder
    pf.purge_old(login, folder='INBOX.LinkedIn', age=2)

@rule
def old_ads(account):
    login = account.login()
    pf.purge_old(login, folder="INBOX.Approved_Ads", age=30)

@rule
def old_heads(account):
    login = account.login()
    pf.purge_old(login, folder="INBOX.HeadHunt", age=30)

@rule
def delete_junk(account):
    login = account.login()
    pf.purge_old(login, folder="INBOX.Junk", age=14)


rules_list = [item for item in rule.registry]