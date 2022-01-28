import re
import sys

INPUT = """
 // my  program in C++

#include <iostream>
/** playing around in
a new programming language **/
using namespace std;

int main ()
{
  cout << "Hello World";
  cout << "I'm a C++ program"; //use cout
  return 0;
}
"""


lines = ""
for line in sys.stdin:
    lines += line.strip()+"\n"

comment = r"(//.*|/\*[\s\S]*?\*/)"
matches = re.findall(comment, lines)
print(*matches, sep="\n")
