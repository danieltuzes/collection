import re
import sys

next(sys.stdin)

languages = {"C", "CPP", "JAVA", "PYTHON", "PERL", "PHP", "RUBY", "CSHARP", "HASKELL", "CLOJURE", "BASH", "SCALA", "ERLANG",
             "CLISP", "LUA", "BRAINFUCK", "JAVASCRIPT", "GO", "D", "OCAML", "R", "PASCAL", "SBCL", "DART", "GROOVY", "OBJECTIVEC"}

for line in sys.stdin:
    pattern = r"^(\d+) ([A-Z]+)"
    match = re.findall(pattern, line)
    if match and match[0][1] in languages and 10**4 < int(match[0][0]) < 10**5:
        print("VALID")
    else:
        print("INVALID")
