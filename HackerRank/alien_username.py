import re
import sys

lines = []
for line in sys.stdin:
    lines.append(line.strip())

n_tests = int(lines[0])
tests = lines[1:1+n_tests]

for test in tests:
    matches = re.findall(r"^[_\.]\d+[a-zA-Z]*_?$", test)
    if matches:
        print("VALID")
    else:
        print("INVALID")
