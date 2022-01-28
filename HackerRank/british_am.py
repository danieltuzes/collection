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
    test_s = r"(\w+)[sz]e"
    sub = r"(\1ze|\1se)"
    find_s = re.sub(test_s, sub, test)
    n_matches = 0
    for line in lines:
        matches = re.findall(find_s, line)
        n_matches += len(matches)
    print(n_matches)
