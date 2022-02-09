"""Notify users if they use a lot of space.

The list of users must be stored in file
defined by the filename stored as the keys of
SERVER_CONF. The file must contain the users and
disk usage as 

```html
<html>
username1	87
username2	11
</html>
```

where the 1st column is the username, from which the e-mail address can be
deduced, and the 2nd column is the used disk space in KB.
"""

import sys
import smtplib
from email.message import EmailMessage
from typing import Dict, Tuple

# region settings
TB_3_5 = 3.5 * 1024 * 1024 * 1024

# the key is the filename where the disk usage is stored
# the value is tuple, whose 0th element is the server name,
# the 1st element is where further information can be obtained, e.g. the
# server's dashboard address, and the 2nd element is the total
# space of the server
SERVER_CONF = {"disk_usage1.html": ("first", "http://first:5000", TB_3_5),
               "disk_usage2.html": ("second", "http://second:5000", TB_3_5)}


# notify the user if uses this ratio of the total space, between [0,1]
USER_TRIGGER = 0.0

# notify the user if the used disk size is larger than this ratio
SPACE_TRIGGER = 0.0

EMAIL_DOMAIN = "@gmail.com"

# overwrite default e-mails as username@domain
EMAIL_ADDR = {"tdani0": "tuzesdaniel+tdani0@gmail.com",
              "danit1": "danieltuzes+danit1@gmail.com",
              "tdannni": "tuzesdaniel+tdanni@gmail.com",
              "tuzesdanit1": "tuzesdaniel+tdanni@gmail.com",
              "danieldanit1": "tuzesdaniel+tdanni@gmail.com",
              "tdani0danit1": "tuzesdaniel+tdanni@gmail.com",
              "danit1danit1": "tuzesdaniel+tdanni@gmail.com"}

METHOD = ["console", "email"]  # ["email", "console"]
SENDER = "tuzesdaniel@gmail.com"

# endregion


def get_disk_usage(du_fname: str) -> Dict[str, int]:
    """Reads in the disk usage file"""
    with open(du_fname, mode="r", encoding="utf-8") as ifile:
        lines = ifile.read().split("\n")[1:-2]

    usage = {line.split("\t")[0]: int(line.split("\t")[1]) for line in lines}
    return usage


def notify_users(usage: Dict[str, int],
                 server_conf: Tuple[str, str]) -> None:
    """Send email or sprint to screen."""
    for user, disk_u in usage.items():
        p_ratio = disk_u/server_conf[2]  # personal ratio
        if p_ratio > USER_TRIGGER:
            notify(user, usage, server_conf)


def notify(piv_user: str,
           usage: Dict[str, int],
           server_conf: Tuple[str, str, float]) -> None:
    """Notify a specific user."""
    email_text = EmailMessage()
    email_text["From"] = SENDER

    rec_addr = EMAIL_ADDR.get(piv_user, f"{piv_user}{EMAIL_DOMAIN}")

    email_text["To"] = rec_addr
    email_text["Subject"] = "Disk usage notification"

    body = ("You've got this mail because the server disk usage on "
            f"'{server_conf[0]}' has reached {SPACE_TRIGGER*100}% and you "
            f"consume more than {USER_TRIGGER*100}% of this space. "
            "List of users and their usage:\n<pre>"
            "       ID\tusage [%]\n")
    for user, disk_u in usage.items():
        perc = int(disk_u/server_conf[2]*100)
        if user == piv_user:
            body += f"you -> {user}\t{perc}\n"
        else:
            body += f"       {user}\t{perc}\n"
    body += (f"\n</pre>Visit {server_conf[1]} for more info.")

    email_text.set_content(body, subtype='html')

    if "email" in METHOD:
        try:
            smtp_obj = smtplib.SMTP('localhost')
            smtp_obj.send_message(email_text)
            print("Successfully sent email")
        except smtplib.SMTPException as err:
            print(f"Error: unable to send email. Error message: {err}")
    if "console" in METHOD:
        print(email_text)


def main() -> None:
    """C-style"""
    for du_file, server_conf in SERVER_CONF.items():
        usage = get_disk_usage(du_file)
        ratio = sum(usage.values()) / server_conf[2]
        if ratio > SPACE_TRIGGER:
            notify_users(usage, server_conf)


if __name__ == "__main__":
    sys.exit(main())
