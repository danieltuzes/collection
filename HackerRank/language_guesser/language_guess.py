import re
import sys

INPUT1 = open("cexamples.txt", encoding="utf-8")
INPUT2 = open("javaexamples.txt", encoding="utf-8")
INPUT3 = open("pythonexamples.txt", encoding="utf-8")

for line in INPUT3:
    c_inc = r"#include"
    c_print = r"printf"

    j_inc = r"import\sjava"
    j_print = r"println"

    p_def = r"def\s.*:"
    p_print = r'print ".*"'

    if re.search(c_inc, line) or re.search(c_print, line):
        print("C")
        break
    if re.search(j_inc, line) or re.search(j_print, line):
        print("Java")
        break
    if re.search(p_def, line) or re.search(p_print, line):
        print("Python")
        break
