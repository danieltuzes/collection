"""Search SO for new questions.

If verification is needed,
open the page and let's hope it goes away the next time.

If new question is found, open the page."""

import json
import subprocess
import sys
import time
import urllib.request
from bs4 import BeautifulSoup

PAGES = [r"https://stackoverflow.com/questions/tagged/numpy%2brandom?tab=Newest",
         r"https://stackoverflow.com/questions/tagged/gnuplot?tab=Newest",
         r"https://stackoverflow.com/questions/tagged/python%2brandom?tab=Newest",
         r"https://stackoverflow.com/questions/tagged/mt19937?tab=Newest",
         r"https://stackoverflow.com/questions/tagged/random-seed?tab=Newest"]

HISTORY_PATH = "last_questions.txt"

BROWSER_PATH = r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
BROWSER_ARGS = r"-private-window"

WAIT = 100


def bs_parse(address: str) -> BeautifulSoup:
    """Properly obtain html code."""
    with urllib.request.urlopen(address) as content_f:
        my_bytes = content_f.read()
        my_str = my_bytes.decode("utf8")
        content_f.close()

    return BeautifulSoup(my_str, "html.parser")


def load_first_question() -> dict[str, str]:
    """Load the last questions' excerpt from file."""
    first_question = {}
    try:
        with open(HISTORY_PATH, mode="r", encoding="utf-8") as ifile:
            first_question = json.load(ifile)
    except FileNotFoundError as err:
        print(f"Cannot find {HISTORY_PATH}. "
              "All first questions are treated as new. "
              f"Error message:\n{err}")

    for page in PAGES:
        if page not in first_question:
            first_question[page] = ""

    return first_question


def save(first_question: dict[str, str]) -> None:
    with open(HISTORY_PATH, mode="w", encoding="utf-8") as ofile:
        json.dump(first_question, ofile, sort_keys=True)


def main() -> int:
    """C-like style."""

    first_question = load_first_question()
    while True:
        for page in PAGES:
            parsed = bs_parse(page)  # parsed html content

            while "verification" in parsed.findAll("title")[0].string:
                print('\r\a')
                print(f"{page} requires authentication. "
                      "I open it in a browser...")
                time.sleep(2)
                subprocess.run([BROWSER_PATH, BROWSER_ARGS, page], check=False)
                time.sleep(5)
                parsed = bs_parse(page)

            first_q_now = parsed.findAll("div",
                                         {"class": "excerpt"})[0].string

            if first_q_now != first_question[page]:
                print('\r\a')
                print(f"{page} has a new question. I open it in a browser...")
                subprocess.run([BROWSER_PATH, page], check=False)
                first_question[page] = first_q_now
                save(first_question)
            else:
                print(f"No new question on {page}")

        print(f"Wait {WAIT} s before retrying.")
        time.sleep(WAIT)


if __name__ == "__main__":
    sys.exit(main())
