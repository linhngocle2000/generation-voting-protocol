import argparse
import sys
import datetime
from ppsim import Simulation
from tabulate import tabulate
import logging
from generation_voting import generation_voting, init_agents_random, one_opinion

time_str = datetime.datetime.now().strftime("%Y%m%d")
logging.basicConfig(filename='logs/simulation-{0}.log'.format(time_str),
                    encoding='utf-8',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def get_args():
    opinion_limit: int = 2

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--level_limit", help="How high is the permissible maximum level increase?",
                        required=True, default="")
    parser.add_argument("-n", "--number_of_agents", help="Number of participating agents",
                        required=True, default="")
    parser.add_argument("-o", "--opinion_limit", help="How high is the permissible maximum opinion?",
                        required=False, default="")

    argument = parser.parse_args()

    try:
        level_limit = int(format(argument.level_limit))
        number_of_agents = int(format(argument.number_of_agents))
        if argument.opinion_limit:
            opinion_limit = int(format(argument.opinion_limit))
    except ValueError:
        sys.exit("All arguments must be integers. Exit.")

    if not (level_limit > 0 and number_of_agents > 0 and opinion_limit > 0):
        sys.exit("All arguments must be bigger than 0. Exit.")

    logging.info("Level limit: {0}; Number of agents: {0}; Opinion limit: {0}"
                 .format(level_limit, number_of_agents, opinion_limit))
    return level_limit, number_of_agents, opinion_limit


def main():
    args = get_args()
    # Initialize simulator with 30 agents with opinions ranging from 1 to 5 and level limit set to 10
    sim = Simulation(init_agents_random(args[1], args[2]), generation_voting, level_limit=args[0])
    # Run simulator until all agents agree on one opinion
    sim.run(one_opinion)
    # Print simulation history group by opinions
    logging.info("\n"+tabulate(sim.history.groupby('opinion', axis=1).sum(), headers='keys', tablefmt='psql'))


if __name__ == "__main__":
    main()
