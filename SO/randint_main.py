import sys
import numpy
numpy.random.seed(100)

if __name__ == "__main__":
    x, y, z = [int(val) for val in sys.argv[1:4]]
    rnd_mat = numpy.random.uniform(low=0, high=1, size=(x, y, z))
    print(rnd_mat)
