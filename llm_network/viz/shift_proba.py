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


class ShiftMatrix(object):
    def _manipulate(self, f, accept, reject, total):
        data = json.load(open(f))

        for l in data:
            d_op = l[0]
            o_op = l[1]
            result = l[2]

            if d_op == o_op:
                continue

            total[d_op][o_op] += 1

            if result == "accept":
                accept[d_op][o_op] += 1
            elif result == "reject":
                reject[d_op][o_op] += 1

        return accept, reject, total

    def __init__(self, filename: object):
        """
        :param model: The model object
        :param trends: The computed simulation trends
        """

        self.data = {}
        c = 0

        accept = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]

        reject = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]

        total = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]

        if isinstance(filename, list):
            for f in filename:
                accept, reject, total = self._manipulate(f, accept, reject, total)

        else:
            accept, reject, total = self._manipulate(filename, accept, reject, total)

        for i in range(len(total)):
            d = total[i]
            for j in range(len(d)):
                if d[j] > 0:
                    accept[i][j] /= d[j]
                    reject[i][j] /= d[j]
        self.data = {"accept": accept, "reject": reject}

    def plot(self, filename=None, d="accept"):
        """
        Generates the plot

        :param filename: Output filename
        :param percentile: The percentile for the trend variance area
        """

        fig, ax = plt.subplots()
        ax.matshow(self.data[d], cmap="Greys", extent=(0, 7, 7, 0))
        ax.grid(color="w", linestyle="-", linewidth=2, which="minor")

        # red box
        plt.hlines(-0, -0, 3, linewidth=4.5, color="red")
        plt.hlines(3, -0, 3, linewidth=3, color="red")
        plt.vlines(-0, -0, 3, linewidth=4.5, color="red")
        plt.vlines(3, -0, 3, linewidth=3, color="red")

        # greeen
        plt.hlines(4, 4, 7, linewidth=3, color="green")
        plt.hlines(7, 4, 7, linewidth=4.5, color="green")
        plt.vlines(4, 4, 7, linewidth=3, color="green")
        plt.vlines(7, 4, 7, linewidth=4.5, color="green")

        # blue
        plt.hlines(0, 4, 7, linewidth=4.5, color="blue")
        plt.hlines(3, 4, 7, linewidth=3, color="blue")
        plt.vlines(4, -0, 3, linewidth=3, color="blue")
        plt.vlines(7, -0, 3, linewidth=4.5, color="blue")

        # yellow
        plt.hlines(4, 0, 3, linewidth=3, color="yellow")
        plt.vlines(-0, 4, 7, linewidth=4.5, color="yellow")
        plt.hlines(7, 0, 3, linewidth=4.5, color="yellow")
        plt.vlines(3, 4, 7, linewidth=3, color="yellow")
        # print(self.data[d])

        for (i, j), z in np.ndenumerate(self.data[d]):
            if i != j:
                ax.text(
                    j + 0.5,
                    i + 0.5,
                    "{:0.2f}".format(z),
                    ha="center",
                    va="center",
                    bbox=dict(boxstyle="round", facecolor="white", edgecolor="0.3"),
                    size=7,
                    alpha=0.8,
                )

        major_ticks = np.arange(0.5, 7.5, 1)
        minor_ticks = np.arange(0, 7, 1)

        ax.set_xticks(major_ticks)
        ax.set_xticks(minor_ticks, minor=True)
        ax.set_yticks(major_ticks)
        ax.set_yticks(minor_ticks, minor=True)

        ax.set_xticklabels(
            [
                "Strongly\n Disagree",
                "Disagree",
                "Mildly\n Disagree",
                "Neutral",
                "Mildly\n Agree",
                "Agree",
                "Fully\n Agree",
            ],
            ha="left",
            rotation=90,
            size=8,
        )

        ax.set_yticklabels(
            [
                "Strongly\n Disagree",
                "Disagree",
                "Mildly\n Disagree",
                "Neutral",
                "Mildly\n Agree",
                "Agree",
                "Fully\n Agree",
            ],
            size=8,
            va="center",
        )

        ax.xaxis.set_ticks_position("bottom")

        plt.xlabel("Opponent")
        plt.ylabel("Discussant")

        model = filename.split("_")[-1].split(".")[0]
        variant = filename.split("_")[-2]

        plt.title(f"[{model}|{variant}] Discussant {d} rate given Opponent stance")

        plt.tight_layout()
        if filename is not None:
            plt.savefig(filename)
            plt.clf()
        else:
            plt.show()
