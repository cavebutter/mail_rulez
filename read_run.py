import rules
import functions as pf
from functions import Account, Mail, Rule
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

account_list = []
for section in config.sections():
    acct = Account(config[section]["server"],config[section]["email"], config[section]["password"])
    account_list.append(acct)


for account in account_list:
    for rule in rules.rules_list:
        rule(account)

    pf.process_inbox(account)