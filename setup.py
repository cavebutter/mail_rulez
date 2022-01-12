

"""Establishes configuration file and allows editing of same"""
import os
import configparser
from functions import Account
import sys

if not os.path.isfile("config.ini"):
    section = input("""Welcome to Mail-Rulez!
    It looks like you're just getting started.  What should we call your first email account?\n""").capitalize()
    server = input("""Please enter the complete address of your account's imap server (e.g. 'imap.example.com').\n""").lower()
    email = input("""Please enter the complete email address that we'll be using for this account (e.g. 'person@example.com')\n""")
    password = input("""Please enter the password for your email account.  Please be assured that your password always stays between your computer and your email provider.  Mail-Rulez never sees your passord. \n""")
    account = Account(server, email, password)

    print("Now, we're going to check to see if we can access your account with the credentials you provided.")

    try:
        account.login()
        proceed = ''
        while proceed not in ("y","n"):
            proceed = input("Success!\nWould you like to proceed?(y/n)").lower()
        if proceed == "n":
            sys.exit()
        elif proceed == "y":
            config = configparser.ConfigParser()
            config.add_section(section)
            config[section]['server'] = server
            config[section]['email'] = email
            config[section]['password'] = password

            with open("config.ini", 'w') as f:
                config.write(f)

            print("""Your first account is properly set up.  We recommend getting used to Mail-Rulez with a single account before branching out.""")


    except:
        print("""We couldn't log in to you email account with the credentials you provided.  Please check your credentials and run setup again.""")
        sys.exit()


elif os.path.isfile("config.ini"):
    section = input("""It looks like you want to edit your configuration file.""")