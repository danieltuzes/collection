import numpy
import ctypes


numpy.random.seed(0)
for i in range(3):
    state = numpy.random.get_state()
    num = numpy.random.randint(0, 2**64, dtype=numpy.uint64)
    print(num, bin(num), sep="\t")
print()

for i in range(3):
    state = numpy.random.get_state()
    num = numpy.random.randint(0, 2**32, dtype=numpy.uint32)
    print(num, bin(num), sep="\t")
print()

for i in range(3):
    state = numpy.random.get_state()
    num = numpy.random.random()
    repres = bin(ctypes.c_ulong.from_buffer(ctypes.c_double(num)).value)
    print(num, repres, sep="\t")
