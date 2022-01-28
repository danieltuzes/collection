import re
import sys

n_lines = int(sys.stdin.readline())

lines = []
for _ in range(n_lines):
    lines.append(sys.stdin.readline())

n_tests = int(sys.stdin.readline())
tests = []

for _ in range(n_tests):
    test = sys.stdin.readline().strip()
    test_s = r"(\w+)our(\w*)"
    sub = r"(\1or\2|\1our\2)"
    find_s = r"\b" + re.sub(test_s, sub, test)+r"\b"
    n_matches = 0
    for line in lines:
        matches = re.findall(find_s, line)
        n_matches += len(matches)
    print(n_matches)
