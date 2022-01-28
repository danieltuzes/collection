import re
import sys

next(sys.stdin)

pattern = r"(\d{1,3})[ \-](\d{1,3})[ \-](\d{4,10})"
sub = r"CountryCode=\1,LocalAreaCode=\2,Number=\3"

for line in sys.stdin:
    out = re.sub(pattern, sub, line)
    print(out.strip())
