from math import ceil, floor

import matplotlib.pyplot as plt
from ipywidgets.widgets import widget
import PyQt5

from ppsim import Simulation
import ipywidgets as widgets


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
    print(sim.config_dict)
    print(sim.config_array)
    sim.run(three_consecutive_values, 0.1)

    # print(sim.history)
    def plot_row(row):
        fig, ax = plt.subplots(figsize=(12, 5))
        sim.history.iloc[row].plot(ax=ax, kind='bar',
                                   title=f'Discrete averaging at time {sim.history.index[row]:.2f}',
                                   xlabel='minute',
                                   ylim=(0, n))

    bar = widgets.interact(plot_row, row=widgets.IntSlider(
        min=0, max=len(sim.history) - 1, step=1, value=0, layout=widgets.Layout(width='100%')))
    plt.show()


if __name__ == '__main__':
    main()
