from imap_tools import MailBox, AND, errors
from dotenv import load_dotenv
import os
from process_folder import process_folder

if __name__ == "__main__":

    # Variables
    load_dotenv()
    server = os.getenv("server")
    account = os.getenv("jayco")
    password = os.getenv("jaypass")

    junk = process_folder("lists/black.txt", server, account, password, "INBOX.Rejected", "INBOX.Junk")
    print(junk)