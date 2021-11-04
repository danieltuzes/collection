# https://stackoverflow.com/questions/69837611/generate-list-of-random-floats-in-a-sequence-for-mocking-iot-sensor/69846502#69846502

import numpy as np
np.random.seed(0)


def gen_rnd_sensor_data(low: float,
                        high: float,
                        n_incr: int,
                        n_decr: int) -> np.ndarray:
    incr = np.random.uniform(low=low, high=high, size=n_incr)
    incr.sort()
    decr = np.random.uniform(low=low, high=high, size=n_decr)
    decr[::-1].sort()
    return np.concatenate((incr, decr))


print(gen_rnd_sensor_data(0, 1, 5, 3))
