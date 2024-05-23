import os
import matplotlib as mpl
import json
from collections import defaultdict
import numpy as np

if os.environ.get("DISPLAY", "") == "":
    print("no display found. Using non-interactive Agg backend")
    mpl.use("Agg")
import matplotlib.pyplot as plt


__author__ = "Giulio Rossetti"
__license__ = "BSD-2-Clause"
__email__ = "giulio.rossetti@gmail.com"


class OpinionEvolution(object):
    def __init__(self, filename: object):
        """
        :param model: The model object
        :param trends: The computed simulation trends
        """

        self.data = {}
        c = 0
        with open(filename) as file:
            for l in file:
                l = json.loads(l)
                if c == 0:
                    vals = l["status"]
                    for k, v in vals.items():
                        if k not in self.data:
                            self.data[k] = []
                        self.data[k].append(v)
                    c += 1
                else:
                    node = l["interacting_agents"]["discussant"]
                    opinion = l["status"][node]
                    self.data[node].append(opinion)

    def plot(self, filename=None):
        """
        Generates the plot

        :param filename: Output filename
        :param percentile: The percentile for the trend variance area
        """
        color_dict = {
            "#ff0000": np.zeros(4),
            "#00ff00": np.zeros(4),
            "#0000ff": np.zeros(4),
        }
        for node, opinions in self.data.items():
            color = "#000000"
            if opinions[0] < 2:
                color = "#ff0000"
            elif 2 <= opinions[0] <= 4:
                color = "#00ff00"
            else:
                color = "#0000ff"

            plt.plot(range(0, len(opinions)), opinions, lw=1, alpha=0.5, color=color)
        #  print(np.array(opinions[:4]))
        #   color_dict[color] += np.array(opinions[:4])

        # print(color_dict)

        plt.xlabel("Iterations", fontsize=24)
        plt.ylabel("Opinion", fontsize=24)
        plt.legend(loc="best", fontsize=18)

        #        plt.tight_layout()
        if filename is not None:
            plt.savefig(filename)
            plt.clf()
        else:
            plt.show()
