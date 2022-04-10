"""Egy véges bináris fában minden csúcsponton x uint értékek vannak.
Határozd meg, hogy a gráfon egy irányban az
elejétől a végéig végighaladva mennyi a maximuma az x értékek
összegének vagy szorzatának, és ez mikből áll össze!

Adj meg egy konstruktort, amivel létre lehet hozni az objektumot!"""

from operator import add, mul
import sys
from typing import Callable, List, Tuple


class node:
    def __init__(self,
                 vals: List[int]) -> None:
        self.val = vals.pop(0)
        if self.val is None:
            return

        self.left = node(vals)
        self.right = node(vals)

    def getmax(self,
               operand: Callable[[int, int], int]) -> Tuple[int, list[int]]:
        """type = sum | prod"""
        if self.val is None:
            return None, []

        leftval, maxpath_l = self.left.getmax(operand)
        rightval, maxpath_r = self.right.getmax(operand)

        if leftval is None and rightval is None:
            return self.val, [self.val]
        if rightval is not None and (leftval is None or rightval > leftval):
            maxpath_r.append(self.val)
            return operand(rightval, self.val), maxpath_r

        # leftval is not None and (rightval is None or rightval <= leftval)
        maxpath_l.append(self.val)
        return operand(leftval, self.val), maxpath_l


def main() -> None:
    """docs"""
    tree = [1, 2, 4, 8, None, None, None, 30, None, None, 3, None, None]
    thenode = node(tree)
    print(thenode.getmax(add))
    print(thenode.getmax(mul))


if __name__ == "__main__":
    sys.exit(main())
