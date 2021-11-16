# MailRulez

##Mail_Sort
Fetch all mail;

If sender is on blacklist, delete;

If sender is on white list, move to /Processed;

If sender is new, move to /Pending;

##User Actions
Move bad mail from /Pending to /Rejected;

Move good mail from /Pending to /Approved;



##Maintain black list
Fetch all mail from /Rejected;

Add sender to blacklist;

Delete Mail

##Maintain white list
Fetch all mail from /Approved;

Add sender to Whitelist;

Move mail to /Processed