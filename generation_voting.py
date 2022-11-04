import random
from dataclasses import dataclass
from matplotlib import pyplot as plt
from ppsim import Simulation, time_trials
from tabulate import tabulate
import seaborn as sns


# Define class Agent.
# Each agent has an opinion and a level, which is initially set to 0.
@dataclass(unsafe_hash=True)
class Agent:
    opinion: int = 0
    level: int = 0

    # Function to print agent.
    def __str__(self):
        s = str(self.opinion) + "(" + str(self.level) + ")"
        return s


# Generation voting protocol that takes 2 agents and 1 level limit.
# Level limit is required since the class Simulation enumerates all possible states
# in its initialization phase before starting a simulation.
# Not stating a level limit would cause the simulator to list out the infinite
# combinations of opinion and level, which increases indefinitely in the protocol,
# and the simulator would never start.
def generation_voting(v: Agent, u: Agent, level_limit: int):
    # Checks if the levels are under limit to make sure that the simulator would run.
    if u.opinion == v.opinion and u.level == v.level <= level_limit:
        u.level += 1
        v.level += 1
    elif u.level > v.level:
        v.opinion = u.opinion
        v.level = u.level
    elif u.level < v.level:
        u.opinion = v.opinion
        u.level = v.level


# Define converging condition: When there is ONLY 1 unique opinion
def one_opinion(config):
    unique_opinions = set(state.opinion for state in config.keys())
    return len(unique_opinions) == 1


# Initialize agent population
# Assign a random opinion to each agent, which is an int between 1 and limit
def init_agents_random(number_of_agents: int, limit: int = 3):
    agents_list = {}
    count = 0
    while count < number_of_agents:
        current_random_int = random.randint(1, limit)
        if Agent(opinion=current_random_int) in agents_list:
            agents_list[Agent(opinion=current_random_int)] += 1
        else:
            agents_list[Agent(opinion=current_random_int)] = 1
        count += 1
    return agents_list


# Another initialize method
# Specify how many agents have opinion 1 and opinion -1
def init_agents(a: int, b: int):
    return {Agent(opinion=1): a, Agent(opinion=-1): b}


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
