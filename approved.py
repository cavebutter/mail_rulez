from imap_tools import MailBox, AND, errors
from dotenv import load_dotenv
import os
from functions import process_folder

if __name__ == "__main__":

    # Variables
    load_dotenv()
    server = os.getenv("server")
    account = os.getenv("account")
    password = os.getenv("password")

    approve = process_folder("lists/white.txt", server, account, password, "INBOX._Approved", "INBOX.Processed")
    print(approve)