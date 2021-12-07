import rules as r
import functions as pf

#  TODO look for way to more easily configure which lists to load- maybe specify in a list and loop thru?
def process_inbox(account, folder="INBOX", limit=100):
    """
    Fetches mail from specified server/account and folder.  Compares the from_ attribute against specified sender lists.
    If a sender matches an address in a specified list, message is dispositioned according to defined rules.  If no match,
    mail is sent to Pending folder.
    """
    # Process special rules
    for rule in r.rules_list:
        rule(account)

    mail_list = []
    log = {}
    log["process"] = "Process Inbox"
    # Load Lists
    # Would it make any difference in terms of memory usage to load these lists when needed?
    whitelist = pf.open_read("/home/sally/mail-rulez/lists/white.txt")
    blacklist = pf.open_read("/home/sally/mail-rulez/lists/black.txt")
    vendorlist = pf.open_read("/home/sally/mail-rulez/lists/vendor.txt")
    headlist = pf.open_read("/home/sally/mail-rulez/lists/head.txt")

    log["whitelist count"] = len(whitelist)
    log["blacklist count"] = len(blacklist)
    log["vendorlist count"] = len(vendorlist)
    log["headlist count"] = len(headlist)
    #  Fetch mail
    mb = account.login()
    mail_list = pf.fetch_class(mb)

    log["mail_list count"] = len(mail_list)

    #  Build list of uids to move to defined folders
    whitelisted = [item.uid for item in mail_list if item.from_ in whitelist]
    blacklisted = [item.uid for item in mail_list if item.from_ in blacklist]
    vendorlist = [item.uid for item in mail_list if item.from_ in vendorlist]
    headlisted = [item.uid for item in mail_list if item.from_ in headlist]
    log["uids in whitelist"] = whitelisted
    log["uids in blacklist"] = blacklisted
    log["uids in vendorlist"] = vendorlist
    log["uids in headlist"] = headlisted
    #  Move email
    mb.move(whitelisted, "INBOX.Processed")
    mb.move(blacklisted, "INBOX.Junk")
    mb.move(vendorlist, "INBOX.Approved_Ads")
    mb.move(headlisted, "INBOX.HeadHunt")

    if folder == "INBOX":
        #  Build list of uids to move to Pending folder
        pending = [item.uid for item in mail_list if item.from_ not in whitelist if item.from_ not in blacklist if
                   item.from_ not in vendorlist]
        log["uids in pending"] = pending

        mb.move(pending, "INBOX.Pending")
    else:
        pass

    return log

def process_inbox_maint(account, folder="INBOX", limit=500):
    """
    Fetches mail from specified server/account and folder.  Compares the from_ attribute against specified sender lists.
    If a sender matches an address in a specified list, message is dispositioned according to defined rules.  If no match,
    mail is sent to Pending folder.
    """
    # Process special rules
    for rule in r.rules_list:
        rule(account)

    mail_list = []
    log = {}
    log["process"] = "Process Inbox"
    # Load Lists
    # Would it make any difference in terms of memory usage to load these lists when needed?
    whitelist = pf.open_read("/home/sally/mail-rulez/lists/white.txt")
    blacklist = pf.open_read("/home/sally/mail-rulez/lists/black.txt")
    vendorlist = pf.open_read("/home/sally/mail-rulez/lists/vendor.txt")
    headlist = pf.open_read("/home/sally/mail-rulez/lists/head.txt")

    log["whitelist count"] = len(whitelist)
    log["blacklist count"] = len(blacklist)
    log["vendorlist count"] = len(vendorlist)
    log["headlist count"] = len(headlist)
    #  Fetch mail
    mb = account.login()
    mail_list = pf.fetch_class(mb)

    log["mail_list count"] = len(mail_list)

    #  Build list of uids to move to defined folders
    whitelisted = [item.uid for item in mail_list if item.from_ in whitelist]
    blacklisted = [item.uid for item in mail_list if item.from_ in blacklist]
    vendorlist = [item.uid for item in mail_list if item.from_ in vendorlist]
    headlisted = [item.uid for item in mail_list if item.from_ in headlist]
    log["uids in whitelist"] = whitelisted
    log["uids in blacklist"] = blacklisted
    log["uids in vendorlist"] = vendorlist
    log["uids in headlist"] = headlisted
    #  Move email
#    mb.move(whitelisted, "INBOX.Processed")
    mb.move(blacklisted, "INBOX.Junk")
    mb.move(vendorlist, "INBOX.Approved_Ads")
    mb.move(headlisted, "INBOX.HeadHunt")

    if folder == "INBOX":
        #  Build list of uids to move to Pending folder
        pending = [item.uid for item in mail_list if item.from_ not in whitelist if item.from_ not in blacklist if
                   item.from_ not in vendorlist]
        log["uids in pending"] = pending

        mb.move(pending, "INBOX.Pending")
    else:
        pass

    return log
