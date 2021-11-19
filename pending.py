from dotenv import load_dotenv
import functions as pf
import os

###################################################################
#                  WHAT HAPPENS IN THIS MODULE                    #
#                                                                 #
#  Fetches specified number of emails  from Pending and compares  #
#  sender to various lists.  If sender matches an entry on a list #
#  the message is moved to the appropriate folder.  If it does not#
#  match, the message is moved to Pending folder for manual dispo-#
#  sition.  This is a refresh for the pending folder so that not  #
#  all items have to be moved manually out of pending for dispo   #
#                                                                 #
###################################################################



if __name__ == "__main__":
    #  Variables
    load_dotenv()
    server = os.getenv("server")
    account = os.getenv("jayco")
    password = os.getenv("jaypass")

    inbox = pf.process_inbox(server, account, password, "INBOX.Pending")

    print(inbox)
