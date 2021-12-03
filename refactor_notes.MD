## Refactoring Mail-Rulez

### Rule class
Add a class for rules.  Initially, this class was developed to provide a decorator that would add rule functions to a list.  The process inbox functions would then iterate through that rule list to execute those functions.
Now that the class has been created, there might be some opportunities to build it out.

### Account Class
Add a class for accounts.  The thinking is that the main script (currently `mail_rulez_maint.py`) would read the config file and create an Account object for each account listed.
Originally had converted a number of functions (e.g. `fetch_class`) to methods, but I had trouble extending or subclassing the imap_tools.MailBox class, and the methods wouldn't run.
Settled on the one `login()` method below, and re-wrote the other functions to accept the Account.login object instad of account credentials.

#### Account Attributes
*server* : the imap server address for the account (e.g. imap.gmail.com)

*email* : the full email address associated with the account (e.g. email@example.com)

*password* : the password associated with the email address

#### Account Methods
##### Account.login()
Calls the `imap_tools.Mailbox.login()` to return a MailBox object logged in with the account credentials.

### Move from .env to .ini
Next iteration will include a setup program to build the config file.