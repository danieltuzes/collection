"""Interjú kérdés:
össze lehet-e ollózni egy újságpapír szövegét (egyik bemenet)
úgy, hogy egy megadott másik szövegét kapjuk (másik bemenet)?"""


def check_if_subs(m_in: str, m_test: str) -> None:
    """Test if m_in has more chars from everything compared to m_test"""
    chars: dict[str:int] = dict()
    for char in m_in:
        if char in chars:
            chars[char] += 1
        else:
            chars[char] = 1

    for char in m_test:
        if char in chars:
            chars[char] -= 1
            if chars[char] == 0:
                del chars[char]
        else:
            return False

    return True


def check_if_subs2(m_in: str, m_test: str) -> None:
    """Test if m_test can be covered from m_in"""
    chars: dict[str:int] = dict()
    for char in m_test:
        if char in chars:
            chars[char] += 1
        else:
            chars[char] = 1

    for char in m_in:
        if char in chars:
            chars[char] -= 1
            if chars[char] == 0:
                del chars[char]

    if not chars:
        return True

    return False


while True:
    sourcestr = input("Give the source string: ")
    teststr = input("Give the test string: ")
    print(check_if_subs2(sourcestr, teststr))
