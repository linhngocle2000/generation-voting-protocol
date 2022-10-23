from math import ceil, floor

import matplotlib.pyplot as plt
from ppsim import Simulation


def discrete_averaging(a, b):
    avg = (a + b) / 2
    # floor(2.4) = 2
    # ceil(2.4) = 3
    return floor(avg), ceil(avg)


def three_consecutive_values(config):
    # get all states at current step
    states = config.keys()
    # are the current states only 3 consecutive values?
    return max(states) - min(states) <= 2


def main():
    n = 10 ** 6
    # division that results into whole number adjusted to the left in the number line
    # init config : 500.000 0's and 500.000 50's
    sim = Simulation({0: n // 2, 50: n // 2}, discrete_averaging)
    sim.run(three_consecutive_values, 0.1)
    print(sim.history)
    sim.history.plot()
    plt.show()


if __name__ == '__main__':
    main()
