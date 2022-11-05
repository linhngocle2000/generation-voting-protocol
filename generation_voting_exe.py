from matplotlib import pyplot as plt
from ppsim import time_trials
from tabulate import tabulate
import seaborn as sns

from generation_voting import generation_voting, init_agents_random


def main():
    # Initialize simulator with 30 agents with opinions ranging from 1 to 5 and level limit set to 10
    # sim = Simulation(init_agents_random(30, 5), generation_voting, level_limit=10)
    # Run simulator until all agents agree on one opinion
    # sim.run(one_opinion)
    # Print simulation history group by opinions
    # print(sim.history.groupby('opinion', axis=1).sum())
    # sim.history.groupby('opinion', axis=1).sum().plot()
    # plt.show()

    # List of different agent population size
    ns = [3, 9, 27, 81, 243]
    # Level limit: 5
    # Opinion: {1,...,3}
    # 1000 runs for each n
    # max_wall_clock(s): time budget of each n in ns.
    # If this time budget runs out, moves to next n without run num_trials runs.
    # Run protocol for different population size and compare convergence time
    df = time_trials(generation_voting, level_limit=5, ns=ns, initial_conditions=init_agents_random,
                     num_trials=1000, max_wallclock_time=0.05)
    print(tabulate(df, headers='keys', tablefmt='psql'))
    lp = sns.lineplot(x='n', y='time', data=df)
    plt.show()


if __name__ == '__main__':
    main()
