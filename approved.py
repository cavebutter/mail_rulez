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

    approve = process_folder("lists/white.txt", server, account, password, "INBOX.Approved", "INBOX.Processed")
    print(approve)