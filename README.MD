# MailRulez

##STARTING OUT


Starting out, you'll use the `process_inbox` function.  This will help you gain control of your inbox by taking bite-sized chunks of 100 emails out of your inbox and moving them to a folder called Pending.  

In Pending, you can move messages into sorting folders (denoted by a leading `_` character). The sorting folders are _Approved, _Rejected, _Vendor, _HH.  These are explained in the following sections. 

###_Approved
Moving an email from Pending to _Approved will do two things.  First, it will add the sender to `lists/white.txt`- a whitelist that will automatically approve all future emails from that sender.  Second, it will move that message to the Processed folder.

**Consider the Processed folder as a folder full of email that you want.  It's from known good senders.  You can take these messasges and store them in archive folders of your choosing, just read and delete, anything you want.**

Once you're ready to moved to the `maint` script, the Processed folder will go away, and all of your approved email will reamin in your inbox.

###_Rejected
Moving an email from Pending to to _Rejected will add the sender to `lists/black.txt` and eventually move the messasge itself to your junk folder.
The next time your inbox is processed, any mail from a blacklisted sender will move straight to Junk. 

###_Vendor
The purpose of the _Vendor folder is to identify senders from companies that you don't want to go to your Junk folder, but you also don't want them cluttering up your inbox.  For messages in this folder, the sender will be added to `lists/vendor.txt`
and the message will be moved to `Approved_Ads`. By default, messages will remain in the `Approved_Ads` folder for 30 days before being deleted.

###_HH
This stands for Head Hunters.  You never know when you'll want to see what kind of jobs are available out there, but you don't want those messages clogging up your inbox.  For messages that you move to the `_HH` folder, the sender will be added to `lists/head.txt` and the message will be moved to `HeadHunt`, where it will remain for 30 days before being deleted.


##MAINTENANCE
 Once you've gotten your inbox down to a reasonable size (Go for zero!), you can switch from `mail_rulez_startup.py` to `mail_rulez_maint.py`.  The only difference between these two scripts is that `maint` does not use the Processed folder; your inbox will contain both new unprocessed messages as well as approved ones.  You can do your sorting from the inbox if you want, but it's still a good idea to check your Pending folder on a regular basis to sort mail from unknown senders.
 
 ####How to stop `mail_rulez_startup.py` and start `mail_rulez.maint.py`
 First thing to do is stop `mail_rulez_startup.py`.  Open a terminal and find the parent process:
 
 `ps -efa | grep mail_rulez`
 
 That will return a process id number.  Use that number to kill the process:
 `kill <pid>`.
 
 ####Starting `mail_rulez_maint.py`
 #####Get your shebang together
 The shebang (`#!`) on the first line of `mail_rulez_maint.py` needs to point to the Python instance in the virtual environment you set up.  Copy the shebang line from `mail_rulez_startup.py` and paste it on the very first line of `mail_rulez_maint.py`.
 
 #####Make `mail_rulez_maint.py` executable
 Open a terminal and `cd` into the mail-rulez directory.  Type:
 
 `chmod a+x mail_rulez_maint.py`
 
 #####Run the script
 In a terminal window, type the following:
 
 `nohup <path to mail-rulez>/mail_rulez_maint.py &`
 
 The `nohup` command makes it so that the script can continue to run even if the terminal window that called it is closed.  `nohup` = No Hang Up.  The trailing `&` tells the OS to run the script in the background. 