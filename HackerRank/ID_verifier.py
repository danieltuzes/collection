import re
import sys

next(sys.stdin)

for line in sys.stdin:
    if re.findall("[a-z]{0,3}\d{2,8}[A-Z]{3,}", line):
        print("VALID")
    else:
        print("INVALID")
