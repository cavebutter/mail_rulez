from imap_tools import MailBox
from datetime import datetime, timedelta

class Rule:
    def __init__(self):
        self.registry = []

    def __call__(self, m):
        "This method is called when some method is decorated"
        self.registry.append(m)

class Mail:
    def __init__(self, uid, subject, from_, date_str, date):
        self.uid = uid
        self.subject = subject
        self.from_ = from_
        self.date_str = date_str
        self.date = date


class Account():
    def __init__(self, server, email, password):
        self.server = server
        self.email = email
        self.password = password

    def login(self):
        """Login to server account, return mailbox object"""
        mb = MailBox(self.server).login(self.email, self.password)
        return mb

def fetch_class(login, folder="INBOX", age=None):
    """
    Fetches all messages from Account, classes them as Mail, changes date to date(), and returns list of those Mail
    :return: list of Mail
    """
    classed_mail = []
    login.folder.set(folder)
    batch = login.fetch(mark_seen=False, bulk=True, reverse=True, headers_only=True)
    for item in batch:
        item = Mail(item.uid, item.subject, item.from_, item.date_str, item.date)
        classed_mail.append(item)
    for item in classed_mail:
        item.date = item.date.date()
    return classed_mail

def fetch_class_100(login, folder="INBOX", age=None):
    """
    Fetches 100 messages from Account, classes them as Mail, changes date to date(), and returns list of those Mail
    :return: list of Mail
    """
    classed_mail = []
    login.folder.set(folder)
    batch = login.fetch(limit=100, mark_seen=False, bulk=True, reverse=True, headers_only=True)
    for item in batch:
        item = Mail(item.uid, item.subject, item.from_, item.date_str, item.date)
        classed_mail.append(item)
    for item in classed_mail:
        item.date = item.date.date()
    return classed_mail

def purge_old(login, folder, age):
    """Purges all messages in specified folder over a specified age"""
    today = datetime.now().date()
    mail = fetch_class(login, folder=folder, age=age)
    purge = [item.uid for item in mail if today - item.date > timedelta(days=age)]
    login.delete(purge)


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

def process_folder(list_file, account, start_folder, dest_folder):
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
    mb = account.login()
    mail_list = fetch_class(mb, start_folder)

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

