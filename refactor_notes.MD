## Refactoring Mail-Rulez

### Rule class
Add a class for rules.  Initially, this class was developed to provide a decorator that would add rule functions to a list.  The process inbox functions would then iterate through that rule list to execute those functions.
Now that the class has been created, there might be some opportunities to build it out.

### Account Class
Add a class for accounts.  The thinking is that the main script (currently `mail_rulez_maint.py`) would read the config file and create an Account object for each account listed.
Many of the functions in `functions.py` would be converted to methods to more concisely run them with specific account settings.
One of the biggest questions yet to be answered is whether this should subclass `imap_tools.MailBox`.  I am pretty sure that the answer is no, but it's complicated as the first method for this class is to create a MailBox object.

#### Account Attributes
*server* : the imap server address for the account (e.g. imap.gmail.com)

*email* : the full email address associated with the account (e.g. email@example.com)

*password* : the passwprd associated with the email address

#### Account Methods
##### Account.login()
Calls the `imap_tools.Mailbox.login()` to return a MailBox object logged in with the account credentials.
##### Account.fetch_class(self, login, folder="INBOX", age=None)
Fetches mail (headers only) from the specified folder and returns a list of Mail objects with Mail.date as Mail.date.date().
Sets the working folder to `folder`.
Calls `imap_tools.MailBox.fetch()` for the Account with the following parameters:
* mark_seen=False, bulk=True, reverse=True, headers_only=True
##### Account.fetch_class_100(self, login, folder="INBOX", age=None)
Same as above, but with a fetch limit of 100 messages.  This method is meant to be used when taming the inbox, to move bite-sized chunks to a processing folder.
##### Account.purge_old(self, login, folder, age)
Deletes mail in `folder` older than `age`.

Uses `Account.login()` to log in to the specified account, sets folder to `folder`.  Fetches and classes all mail with `Account.fetch_class()`, and deletes all mail older than `age`.
#### Issues with Account Class
