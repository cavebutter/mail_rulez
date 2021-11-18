from imap_tools import MailBox, AND, errors
from dotenv import load_dotenv
import os
import functions as pf
from functions import Mail

###################################################################
#                  WHAT HAPPENS IN THIS MODULE                    #
#                                                                 #
#  Fetches specified number of emails  from INBOX and compares    #
#  sender to various lists.  If sender matches an entry on a list #
#  the message is moved to the appropriate folder.  If it does not#
#  match, the message is moved to Pending folder for manual dispo-#
#  sition.                                                        #
#                                                                 #
###################################################################


#  TODO build log from return function
#  TODO Make an easier configuration option for limit in fetch


if __name__ == "__main__":
    #  Variables
    load_dotenv()
    server = os.getenv("server")
    account = os.getenv("jayco")
    password = os.getenv("jaypass")

    inbox = pf.process_inbox(server, account, password, "INBOX")

    print(inbox)
