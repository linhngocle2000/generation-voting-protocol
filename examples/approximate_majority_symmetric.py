
from ppsim import species, Simulation
from matplotlib import pyplot as plt
import numpy as np


def main():
    a, b, u = 'A', 'B', 'U'
    approximate_majority_symmetric = {
        (a, b): (u, u), (b, a): (u, u),
        (a, u): (a, a), (u, a): (a, a),
        (b, u): (b, b), (u, b): (b, b)
    }
    n = 10 ** 9
    init_config = {a: 0.501 * n, b: 0.499 * n}
    sim = Simulation(init_config, approximate_majority_symmetric)
    sim.run(10, 0.1)
    print(sim.history)
    sim.history.plot()
    plt.title('approximate majority protocol')
    plt.xlim(0, sim.times[-1])
    plt.ylim(0, n)
    plt.show()


if __name__ == '__main__':
    main()
