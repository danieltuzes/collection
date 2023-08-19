import sys
import os
import datetime
import time
import logging
logging.basicConfig(level=logging.INFO)

logging.info("Program started.")
print("This is from print")
for i in range(10):
    with open("ofile.txt", mode="a", encoding="utf-8") as ofile:
        print(f"{i}, {datetime.datetime.now()}",
            f"{os.getcwd()}",
            f"{sys.path}",          
            file=ofile)
        time.sleep(0.3)
logging.info("Program completed.")