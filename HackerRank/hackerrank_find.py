import sys
import re

next(sys.stdin)

endswith = "hackerrank$"
startswith = "^hackerrank"

for line in sys.stdin:
    ends = re.findall(endswith, line)
    starts = re.findall(startswith, line)

    if ends and starts:
        print(0)
    elif ends:
        print(2)
    elif starts:
        print(1)
    else:
        print(-1)
