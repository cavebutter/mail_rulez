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


def process_folder(list_file, server, account, password, start_folder, dest_folder):
    log = {}
    f = open(list_file, "r")
    file_list = f.read().split("\n")
    f.close()
    mb = MailBox(server).login(account, password, initial_folder=start_folder)
    batch = mb.fetch(limit=200, mark_seen=False, bulk=True)
    emails = {msg.uid:msg.from_ for msg in batch}
    email_list = list(emails.items()) # TODO is there a more elegant way to do this?
    new_items = set([item[1] for item in email_list if item[1] not in file_list])
    for item in new_items:
        file_list.append(item)
    f = open(list_file, "w")
    for item in file_list:
        f.write(str(item + "\n"))
    f.close()
    move_mail = [msg[0] for msg in emails]
    mb.move(move_mail, dest_folder)
    now = datetime.now()
    format = "%Y-%m-%d %H:%M:%S"
    event_time = now.strftime(format)
    log["Date"] = event_time
    log["Folder"] = start_folder
    log["New entries Number"] = len(new_items)
    log["New Entries Detail"] = new_items
    log["Mail Moved"] = len(move_mail)

    return log

def rm_blanks(file):
    with open(file, "r+") as f:
        clean = [line for line in f.readlines() if line != "\n"]
        f.seek(0)
        for item in clean:
            f.writelines(item)
        f.truncate()

def open_read(file):
    with open(file, "r") as f:
        list_name = f.read().split("\n")
        f.close()
    return list_name

def remove_entry(item, file):
    with open(file, "r") as f:
        lines = f.readlines()
    with open(file, "w") as g:
        for line in lines:
            if line.strip("\n") != item:
                g.write(line)