import re
import sys

lines = []
for line in sys.stdin:
    lines.append(line.strip())

n_sentences = int(lines[0])
sentences = lines[1:1+n_sentences]

n_queries = int(lines[1+n_sentences])
queries = lines[2+n_sentences:]

for query in queries:
    n_matches = 0
    for sentence in sentences:
        # find subwords of query in sentence
        matches = re.findall(r"(?<=\w)" + query + r"(?=\w)", sentence)
        n_matches += len(matches)
    print(n_matches)
