from ppsim import species, Simulation
from matplotlib import pyplot as plt


def main():
    a, b, u = species('A B U')
    approximate_majority = [
        a + b >> 2 * u,
        a + u >> 2 * a,
        b + u >> 2 * b,
    ]
    n = 10 ** 5
    init_config = {a: 0.51 * n, b: 0.49 * n}
    #sim = Simulation(init_config, approximate_majority)
    #sim.run()
    # transition_order='asymmetric' is when, e.g., (a,b):(u,u) != (b,a):(u,u)
    sim = Simulation(init_config, approximate_majority, transition_order='asymmetric')
    print(sim.reactions)
    sim.run()
    p = sim.history.plot()
    print(sim.history)
    sim.history.plot()
    plt.title('approximate majority protocol')
    plt.xlim(0, sim.times[-1])
    plt.ylim(0, n)
    #plt.show()


if __name__ == '__main__':
    main()
