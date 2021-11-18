from imap_tools import MailBox, AND, errors
from dotenv import load_dotenv
import os
from functions import process_folder

if __name__ == "__main__":

    # Variables
    load_dotenv()
    server = os.getenv("server")
    account = os.getenv("jayco")
    password = os.getenv("jaypass")

    vendor = process_folder("lists/vendor.txt", server, account, password, "INBOX._Vendor", "INBOX.Approved_Ads")
    print(vendor)