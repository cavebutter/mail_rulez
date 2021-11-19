from dotenv import load_dotenv
import os
from functions import process_folder

if __name__ == "__main__":

    # Variables
    load_dotenv()
    server = os.getenv("server")
    account = os.getenv("jayco")
    password = os.getenv("jaypass")

    head = process_folder("lists/head.txt", server, account, password, "INBOX._HH", "INBOX.HeadHunt")
    print(head)