from imap_tools import MailBox, errors
from datetime import datetime



###################################################################
#                  WHAT HAPPENS IN THIS MODULE                    #
#                                                                 #
#  1. Module reads a list of email addresses into memory          #
#  2. Fetch all mail from specified folder and compare sender     #
#     against list                                                #
#  3. For all senders not in the list, add them to the list       #
#  4. Move all emails to the specified dest folder                #
#  5. Separate function to remove blank lines from email lists    #
###################################################################

class Mail:
    def __init__(self, uid, subject, from_, date_str):
        self.uid = uid
        self.subject = subject
        self.from_ = from_
        self.date_str = date_str

def rm_blanks(file):
    """
    Removes blank lines from email list file
    :param file:
    :return:
    """
    with open(file, "r+") as f:
        clean = [line for line in f.readlines() if line != "\n"]
        f.seek(0)
        for item in clean:
            f.writelines(item)
        f.truncate()

def open_read(file):
    """
    Open email list file and read contents into list
    :param file:
    :return: list of addresses
    """
    with open(file, "r") as f:
        list_name = f.read().split("\n")
        f.close()
    return list_name

def remove_entry(item, file):
    """
    Removes a duplicate list entry from user-specified list
    :param item:
    :param file:
    :return:
    """
    with open(file, "r") as f:
        lines = f.readlines()
    with open(file, "w") as g:
        for line in lines:
            if line.strip("\n") != item:
                g.write(line)

def new_entries(file, list):
    """
    Enters new list entries to file
    :param file:
    :param list:
    :return:
    """
    with open(file, "a") as f:
        for entry in list:
            f.write(str(entry) + "\n")

def class_mail(batch):
    """
    Renders each message returned in mailbox fetch to Mail object and adds the object to a list for further processing
    :param batch:
    :return: list of mail objects
    """
    mail_list = []
    for item in batch:
        item = Mail(item.uid, item.subject, item.from_, item.date_str)
        mail_list.append(item)
    return mail_list

#  TODO look for way to more easily configure which lists to load- maybe specify in a list and loop thru?
def process_inbox(server, account, password, folder="INBOX", limit=100):
    """
    Fetches mail from specified server/account and folder.  Compares the from_ attribute against specified sender lists.
    If a sender matches an address in a specified list, message is dispositioned according to defined rules.  If no match,
    mail is sent to Pending folder.
    :param server: FQDN imap server
    :param account: account email
    :param password: account pwd
    :param folder: default = "INBOX"
    :param limit: default = 100
    :return: log of actions
    """
    mail_list = []
    log = {}
    log["process"] = "Process Inbox"
    # Load Lists
    # Would it make any difference in terms of memory usage to load these lists when needed?
    whitelist = open_read("lists/white.txt")
    blacklist = open_read("lists/black.txt")
    vendorlist = open_read("lists/vendor.txt")
    log["whitelist count"] = len(whitelist)
    log["blacklist count"] = len(blacklist)
    log["vendorlist count"] = len(vendorlist)

    #  Fetch mail
    mb = MailBox(server).login(account, password, initial_folder=folder)
    batch = mb.fetch(limit=limit, mark_seen=False, bulk=True, reverse=True, headers_only=True)

    #  Class mail
    mail_list = class_mail(batch)
    log["mail_list count"] = len(mail_list)

    #  Build list of uids to move to defined folders
    whitelisted = [item.uid for item in mail_list if item.from_ in whitelist]
    blacklisted = [item.uid for item in mail_list if item.from_ in blacklist]
    vendorlist = [item.uid for item in mail_list if item.from_ in vendorlist]
    log["uids in whitelist"] = whitelisted
    log["uids in blacklist"] = blacklisted
    log["uids in vendorlist"] = vendorlist

    #  Build list of uids to move to Pending folder
    pending = [item.uid for item in mail_list if item.from_ not in whitelist if item.from_ not in blacklist if item.from_ not in vendorlist]
    log["uids in pending"] = pending
    #  Move email
    mb.move(whitelisted, "INBOX.Processed")
    mb.move(blacklisted, "INBOX.Junk")
    mb.move(vendorlist, "INBOX.Approved_Ads")
    mb.move(pending, "INBOX.Pending")

    return log

def process_folder(list_file, server, account, password, start_folder, dest_folder):
    """
    Processes mail that was manually moved to a sorting folder.  Checks sender against appropriate list.  If sender is
    not in list, sender is added. All mail moved to dest folder.
    :param list_file: email list to check against
    :param server: account imap server
    :param account: account email address
    :param password: account pwd
    :param start_folder: folder to process
    :param dest_folder: dest folder for processed mail
    :return: log
    """
    log = {}
    log["process"] = start_folder
    #  Load List
    file_list = open_read(list_file)

    #  Fetch Mail
    mb = MailBox(server).login(account, password, initial_folder=start_folder)
    batch = mb.fetch(limit=200, mark_seen=False, bulk=True, reverse=True)

    #  Class Mail
    mail_list = class_mail(batch)
    log["mail_list count"] = len(mail_list)

    #  New addresses added to list
    new_list_entries = set([item.from_ for item in mail_list if item.from_ not in file_list])
    new_entries(list_file, new_list_entries)
    rm_blanks(list_file)
    log["New entries Number"] = len(new_list_entries)
    log["New Entries Detail"] = new_list_entries

    #  All messages must be moved
    msgs_to_move = [item.uid for item in mail_list]
    mb.move(msgs_to_move, dest_folder)
    log["Messages Processed"] = len(msgs_to_move)
    log["Diff"] = len(mail_list) - len(msgs_to_move)

    now = datetime.now()
    format = "%Y-%m-%d %H:%M:%S"
    event_time = now.strftime(format)
    log["Date"] = event_time

    return log

