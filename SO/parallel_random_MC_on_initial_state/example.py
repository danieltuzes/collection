import numpy

ss_entropy_1 = numpy.random.SeedSequence(entropy=0)
ss_entropy_2 = numpy.random.SeedSequence(entropy=(0,))

ss_spawn_1 = numpy.random.SeedSequence(entropy=0, spawn_key=(0,))
ss_spawn_2 = numpy.random.SeedSequence(entropy=0, spawn_key=(0,))

ss_spawn_B = numpy.random.SeedSequence(entropy=0, spawn_key=(0,))

prng_seed = numpy.random.Generator(numpy.random.MT19937(0))

ss = numpy.random.SeedSequence(0)
prng_ss = numpy.random.Generator(numpy.random.MT19937(ss))

prng_ss

print("hi")
