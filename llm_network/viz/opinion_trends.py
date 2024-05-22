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


class OpinionTrends(object):
    def __init__(self, filename: object):
        """
        :param model: The model object
        :param trends: The computed simulation trends
        """

        self.data = defaultdict(list)

        with open(filename) as file:

            old_iter = 0
            statuses = {}
            for id_row, l in enumerate(file):

                l = json.loads(l)

                vals = l["status"]
                # try:
                try:
                    iter = l['iteration']
                except:
                    continue

                if iter == old_iter:
                    statuses = l['status']
                else:
                    sts = {k: sum(value == k for value in statuses.values()) for k in range(0, 7)}
                    old_iter = iter
                    for k, v in sts.items():
                        self.data[k].append(v)

        for k, v in self.data.items():
            self.data[k] = [x / len(l['status']) for x in self.data[k]]

    def plot(self, filename=None, limit=None):
        """
        Generates the plot

        :param filename: Output filename
        :param percentile: The percentile for the trend variance area
        """

        label = {
            0: "Strongly Disagree",
            1: "Disagree",
            2: "Mildly Disagree",
            3: "Neutral",
            4: "Mildly Agree",
            5: "Agree",
            6: "Strongly Agree"
        }

        for k in [0, 6, 1, 5, 2, 4, 3]:
            # print(k, self.data[k])
            if limit is None:
                plt.plot(range(0, len(self.data[k])), self.data[k], lw=1, alpha=0.5, label=label[k])
            else:
                plt.plot(range(0, limit), self.data[k][:limit], lw=1, alpha=0.5, label=label[k])

        plt.xlabel("Iterations", fontsize=10)
        plt.ylabel("% Agents", fontsize=10)
        plt.legend(loc="best", fontsize=8, ncol=4, bbox_to_anchor=(0.9, 1.15))

        plt.tight_layout()
        if filename is not None:
            plt.savefig(filename)
            plt.clf()
        else:
            plt.show()
