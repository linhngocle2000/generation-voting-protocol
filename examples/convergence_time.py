import matplotlib.pyplot as plt
from ppsim import time_trials
import numpy as np
import seaborn as sns
from tabulate import tabulate


def main():
    a, b, u = 'A', 'B', 'U'
    approximate_majority = {
        (a, b): (u, u),
        (a, u): (a, a),
        (b, u): (b, b)
    }
    ns = [int(n) for n in np.geomspace(10, 10 ** 8, 3)]
    print(ns)
    df = time_trials(approximate_majority, ns, initial_condition, num_trials=100, max_wallclock_time=30)
    print(tabulate(df, headers='keys', tablefmt='psql'))
    lp = sns.lineplot(x='n', y='time', data=df)
    lp.set_xscale('log')
    plt.show()


def initial_condition(n):
    return {'A': n // 2, 'B': n // 2}


if __name__ == '__main__':
    main()
