import re
import sys

expr = ""
for char in "hackerrank":
    expr += f"[{char}|{char.upper()}]"

count = 0
for line in sys.stdin:
    if re.findall(expr, line):
        count += 1
print(count)
