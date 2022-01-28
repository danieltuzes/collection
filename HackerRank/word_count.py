import re
import sys

lines = []
for line in sys.stdin:
    lines.append(line.strip())

n_sentences = int(lines[0])
sentences = lines[1:1+n_sentences]

n_words = int(lines[1+n_sentences])
words = lines[2+n_sentences:]

for word in words:
    n_matches = 0
    for sentence in sentences:
        matches = re.findall(
            r"\b" + word + r"\b", sentence)
        n_matches += len(matches)
    print(n_matches)
