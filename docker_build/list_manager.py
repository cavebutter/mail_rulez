# Compare the elements of all lists to check for duplicates
# Then ask user to choose which list they want it to remain on
import functions as pf

if __name__ == "__main__":

    #  Remove blank lines from email lists
    pf.rm_blanks("lists/white.txt")
    pf.rm_blanks("lists/black.txt")
    pf.rm_blanks("lists/vendor.txt")
    pf.rm_blanks("lists/head.txt")

    #  Open email lists and read into memory
    black = pf.open_read("lists/black.txt")
    vendor = pf.open_read("lists/vendor.txt")
    white = pf.open_read("lists/white.txt")
    head = pf.open_read("lists/head.txt")

    #  Make list of common emails in each list against each other
    black_vendor = [email for email in black if email in vendor if email != "\n"]
    black_white = [email for email in black if email in white if email != "\n"]
    white_vendor = [email for email in white if email in vendor if email != "\n"]
    head_black = [email for email in head if email in black if email != "\n"]
    head_white = [email for email in head if email in white if email != "\n"]
    head_vendor = [email for email in head if email in vendor if email != "\n"]


    #  Disposition each item
    for item in black_white:
        response = ""
        while response not in ("1","2"):
            response = input(f"{item} is in both blacklist and whitelist.  Where does it belong?\n1. Blacklist\n2. Whitelist\n")
            if response == "1":
                pf.remove_entry(item, "lists/white.txt")
            elif response == "2":
                pf.remove_entry(item, "lists/black.txt")

    for item in black_vendor:
        response = ""
        while response not in ("1","2"):
            response = input(f"{item} is in both blacklist and vendor list.  Where does it belong?\n1. Blacklist\n2. Vendor List\n")
            if response == "1":
                pf.remove_entry(item, "lists/vendor.txt")
            elif response == "2":
                pf.remove_entry(item, "lists/black.txt")

    for item in white_vendor:
        response = ""
        while response not in ("1","2"):
            response = input(f"{item} is in both vendor list and whitelist.  Where does it belong?\n1. Vendor List\n2. Whitelist\n")
            if response == "1":
                pf.remove_entry(item, "lists/white.txt")
            elif response == "2":
                pf.remove_entry(item, "lists/vendor.txt")

    for item in head_black:
        response = ""
        while response not in ("1","2"):
            response = input(f"{item} is in both head list and blacklist.  Where does it belong?\n1. Head List\n2. Blacklist\n")
            if response == "1":
                pf.remove_entry(item, "lists/black.txt")
            elif response == "2":
                pf.remove_entry(item, "lists/head.txt")

    for item in head_white:
        response = ""
        while response not in ("1","2"):
            response = input(f"{item} is in both head list and whitelist.  Where does it belong?\n1. Head List\n2. Whitelist\n")
            if response == "1":
                pf.remove_entry(item, "lists/white.txt")
            elif response == "2":
                pf.remove_entry(item, "lists/head.txt")

    for item in head_vendor:
        response = ""
        while response not in ("1","2"):
            response = input(f"{item} is in both head list and vendor list.  Where does it belong?\n1. Head List\n2. Vendor List\n")
            if response == "1":
                pf.remove_entry(item, "lists/vendor.txt")
            elif response == "2":
                pf.remove_entry(item, "lists/head.txt")