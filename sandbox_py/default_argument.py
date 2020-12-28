"""
    What if I modify the default argument of a function and then I call it again,
    with fallback to default argument? Let's see!

    Tl;dr: yes, it happens, but to mutable types only!
"""


def non_mutable_f(param_a, param_b=0):
    """is b modified in subsequent calls? b is non-mutable, ie. immutable"""
    param_b += param_a
    return param_b


print(non_mutable_f(1), non_mutable_f(1), non_mutable_f(1))
# No, b doesn't change


def mutable_f_arg(param_a, m_list=[]):  # pylint: disable = W0102
    """m_list is mutable, that's dangerous! m_list should be None instead"""
    m_list.append(param_a)
    return m_list


print(mutable_f_arg(1))
print(mutable_f_arg(2))
print(mutable_f_arg(3))


def mutable_f2_arg(param_a, m_list=None):
    """This is the safe way"""
    if m_list is None:
        m_list = []
    m_list.append(param_a)
    return m_list


print(mutable_f2_arg(1))
print(mutable_f2_arg(2))
print(mutable_f2_arg(3))
