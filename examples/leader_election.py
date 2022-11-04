import dataclasses
from dataclasses import dataclass

from matplotlib import pyplot as plt
from ppsim import Simulation

import numpy as np

u = 5
# The parameter unsafe_hash=True makes the state hashable, as required, but still lets the transition code change the field values
# Note that ppsim will by default make safe copies of the agent states before applying the rule,
#  so it is safe to mutate the fields of an agent in the transition rule

@dataclass(unsafe_hash=True)
class Agent:
    role: str = 'contender'
    flip_bit: int = 0
    marker: int = 0
    phase: str = 'marking'
    counter: int = 0


def leader_election(v: Agent, u: Agent, loglogn: int, Ulogn: int):
    # marking phase
    if v.phase == 'marking':
        if v.counter >= 3 * loglogn and u.flip_bit == 0:
            v.phase = 'tournament'
        else:
            v.counter += 1
        if v.counter == 4 * loglogn:
            v.marker = 1
            v.phase = 'tournament'

    if v.phase == 'tournament':
        if v.role == 'contender':
            if u.marker and v.counter <= Ulogn:
                v.counter += 1
            if v.counter < u.counter:
                v.role = 'minion'
            if u.role == 'contender' and v.counter == u.counter and v.flip_bit < u.flip_bit:
                v.role = 'minion'
        v.counter = max(v.counter, u.counter)

    v.flip_bit = 1 - v.flip_bit

    return v


def transition(v: Agent, u: Agent, loglogn: int, Ulogn: int):
    return leader_election(v, dataclasses.replace(u), loglogn, Ulogn), leader_election(u, dataclasses.replace(v),
                                                                                       loglogn, Ulogn)


# ns = [int(n) for n in np.geomspace(10, 10 ** 8, 8)]

# states = []
# for n in ns:
#     sim = Simulation({Agent(): n}, transition, loglogn=int(np.log2(np.log2(n))), Ulogn=u*int(np.log2(n)))
#     states.append(len(sim.state_list))
# plt.plot(ns, states)
# plt.xscale('log')
# plt.xlabel('population size n')
# plt.ylabel('number of states')
# plt.show()

n = 10 ** 9
sim = Simulation({Agent(): n}, transition, loglogn=int(np.log2(np.log2(n))), Ulogn=u * int(np.log2(n)))
print(sim.state_list)


# def one_leader(config):
#     leader_states = [state for state in config.keys() if state.role == 'contender']
#     return len(leader_states) == 1 and config[leader_states[0]] == 1


# sim.run(one_leader)

# sim.history.groupby('role', axis=1).sum().plot()
# plt.yscale('symlog')
# plt.ylim(0, 2*n)
# plt.show()

# sim.history.groupby('phase', axis=1).sum().plot()
# plt.show()
# df = sim.history.groupby(['counter','role'], axis=1).sum()
# print(df.iloc[10].unstack())

# df.iloc[10].unstack().plot(kind='bar', figsize=(12,5))
# plt.show()
