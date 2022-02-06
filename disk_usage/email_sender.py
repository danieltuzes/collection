"""Notify users if they use a lot of space."""

import sys
import time
import subprocess

# region settings
TB_3_5 = 3.5 * 1024 * 1024 * 1024

SERVER_CONF = {"disk_usage1.html": ("first", "http://first:5000", TB_3_5),
               "disk_usage2.html": ("second", "http://second:5000", TB_3_5)}


# notify the user if uses this ratio of the total space
USER_TRIGGER = 0.0

# notify the user if the used disk size is larger than this ratio
SPACE_TRIGGER = 0.0

EMAIL_DOMAIN = "@gmail.com"

# overwrite default e-mails as username@domain
EMAIL_ADDR = {"tdani0": "tuzesdaniel+tdani0@gmail.com",
              "danit1": "danieltuzes+danit1@gmail.com"}

METHOD = ["console"]  # ["email", "console"]

# endregion


def get_disk_usage(du_fname: str) -> dict[str, int]:
    """Reads in the disk usage file"""
    with open(du_fname, mode="r", encoding="utf-8") as ifile:
        lines = ifile.read().split("\n")[1:-2]

    usage = {line.split("\t")[0]: int(line.split("\t")[1]) for line in lines}
    return usage


def notify_users(usage: dict[str, int],
                 server_conf: tuple[str, str]) -> None:
    """Send email or sprint to screen."""
    for user, disk_u in usage.items():
        p_ratio = disk_u/server_conf[2]  # personal ratio
        if p_ratio > USER_TRIGGER:
            notify(user, usage, server_conf)


def notify(piv_user: str,
           usage: dict[str, int],
           server_conf: tuple[str, str, float]) -> None:
    """Notify a specific user."""
    message = ("You've got this mail because the server disk usage on "
               f"'{server_conf[0]}' has reached {SPACE_TRIGGER*100}% and you "
               f"consume more than {USER_TRIGGER*100}% of this space. "
               "List of users and their usage:\n"
               "       ID\tusage [%]\n")
    for user, disk_u in usage.items():
        perc = int(disk_u/server_conf[2]*100)
        if user == piv_user:
            message += f"you -> {user}\t{perc}\n"
        else:
            message += f"       {user}\t{perc}\n"
    message += (f"\nVisit {server_conf[1]} for more info.")

    email = f"{piv_user}{EMAIL_DOMAIN}"
    syscall = ["echo", "-e", message, "|", "sendmail", email]

    if "email" in METHOD:
        subprocess.run(syscall, check=False)
    if "console" in METHOD:
        print(syscall)


def main() -> None:
    """C-style"""
    for du_file, server_conf in SERVER_CONF.items():
        usage = get_disk_usage(du_file)
        ratio = sum(usage.values()) / server_conf[2]
        if ratio > SPACE_TRIGGER:
            notify_users(usage, server_conf)
        time.sleep(1)


if __name__ == "__main__":
    sys.exit(main())
