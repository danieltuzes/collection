import re
import sys

# lines = []
# for line in sys.stdin:
# lines.append(line.strip())

lines = """35
1050:0:0:0:5:600:300c:326b
1050:0:0:0:5:600:300c:326a
1050:0:0:0:5:600:300c:326c
1051:0:0:0:5:600:300c:326b
22.231.113.64
22.231.113.164
255.231.111.64
253.231.111.64
1050:10:0:0:5:600:300c:326b
1050:10:0:0:5:600:300c:326a
1050:10:0:0:5:600:300c:326c
1051:10:0:0:5:600:300c:326b
22.21.113.61
22.21.113.162
255.21.111.63
253.21.111.69
1050:10:0:0:15:600:300c:326b
1050:10:0:10:5:600:300c:326a
1050:10:10:0:5:600:300c:326c
1051:110:0:0:5:600:300c:326b
22.211.113.64
22.212.113.164
255.213.111.64
253.214.111.64
1050:10:0:0:15:600:300c:326k
1050:10:0:0:15:600:300c:326g
1050:10:0:0:15:600:300c:326h
1050:10:0:0:15:600:300c:326i
22.211.113.364
22.212.113.3164
255.213.111.464
253.214.111.564
not an ip address
not an ipv4 Address
Not an IPv5 Address""".split("\n")

output = """IPv6
IPv6
IPv6
IPv6
IPv4
IPv4
IPv4
IPv4
IPv6
IPv6
IPv6
IPv6
IPv4
IPv4
IPv4
IPv4
IPv6
IPv6
IPv6
IPv6
IPv4
IPv4
IPv4
IPv4
Neither
Neither
Neither
Neither
Neither
Neither
Neither
Neither
Neither
Neither
Neither"""


n_tests = int(lines[0])
tests = lines[1:1+n_tests]

for test in tests:
    byte = r'([01]?\d{1,2}|2[0-4]\d|25[0-5])'
    ipv4 = "^" + (byte + r"\.")*3+byte + "$"
    ipv4_match = re.findall(ipv4, test)
    if ipv4_match:
        print("IPv4")
        continue
    hex_g = r"[\da-fA-F]{1,4}"
    ipv6 = "^" + (hex_g + ":")*7+hex_g + "$"
    pv6_match = re.findall(ipv6, test)
    if pv6_match:
        print("IPv6")
    else:
        print("Neither")
