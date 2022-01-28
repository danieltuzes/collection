import re
import sys

next(sys.stdin)

pattern = r"[A-Z]{5}\d{4}[A-Z]"
for line in sys.stdin:
    if re.findall(pattern, line):
        print("YES")
    else:
        print("NO")
