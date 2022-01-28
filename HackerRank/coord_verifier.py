import re
import sys

next(sys.stdin)

for line in sys.stdin:
    Xr = r'[+-]?([0-9](\.[0-9]+)?|[1-8][0-9](\.[0-9]+)?|90(\.0+)?)'
    Yr = r'[+-]?(180(\.0+)?|[0-9](\.[0-9]+)?|[1-9][0-9](\.[0-9]+)?|1[0-7][0-9](\.[0-9]+)?)'
    pattern = r"\(" + Xr + ", " + Yr + r"\)"
    if re.findall(pattern, line):
        print("Valid")
    else:
        print("Invalid")
