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
    def __init__(self, filename: object):
        """
        :param model: The model object
        :param trends: The computed simulation trends
        """

        self.data = {}
        c = 0
        with open(filename) as file:
            file.readline()
            accept = [[0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0]]

            reject = [[0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0]]

            total = [[0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0]]

            for l in file:
                l = json.loads(l)
                d_op = l['interacting_agents']['discussant_opinion']
                o_op = l['interacting_agents']['opponent_opinion']
                d_v_op = l['opinion_variation_discussant']

                total[d_op][o_op] += 1

                if d_op > o_op and d_v_op == -1:
                    accept[d_op][o_op] += 1
                elif d_op < o_op and d_v_op == 1:
                    accept[d_op][o_op] += 1

                if d_op > o_op and d_v_op == 1:
                    reject[d_op][o_op] += 1
                elif d_op < o_op and d_v_op == -1:
                    reject[d_op][o_op] += 1

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
        ax.grid(color='w', linestyle='-', linewidth=2, which="minor")

        #red box
        plt.hlines(-0, -0, 3, linewidth=4.5, color="red")
        plt.hlines(3, -0, 3, linewidth=3, color="red")
        plt.vlines(-0, -0, 3, linewidth=4.5, color="red")
        plt.vlines(3, -0, 3, linewidth=3,  color="red")

        #greeen
        plt.hlines(4, 4, 7, linewidth=3, color="green")
        plt.hlines(7, 4, 7, linewidth=4.5, color="green")
        plt.vlines(4, 4, 7, linewidth=3, color="green")
        plt.vlines(7, 4, 7, linewidth=4.5, color="green")
        
        #blue
        plt.hlines(0, 4, 7, linewidth=4.5, color="blue")
        plt.hlines(3, 4, 7, linewidth=3, color="blue")
        plt.vlines(4, -0, 3, linewidth=3, color="blue")
        plt.vlines(7, -0, 3, linewidth=4.5, color="blue")

        #yellow
        plt.hlines(4, 0, 3, linewidth=3,  color="yellow")
        plt.vlines(-0, 4, 7, linewidth=4.5, color="yellow")
        plt.hlines(7, 0, 3, linewidth=4.5,  color="yellow")
        plt.vlines(3, 4, 7, linewidth=3, color="yellow")
        #print(self.data[d])

        for (i, j), z in np.ndenumerate(self.data[d]):
            if i != j:
                ax.text(j+0.5, i+0.5, '{:0.2f}'.format(z), ha='center', va='center', bbox=dict(boxstyle='round', facecolor='white', edgecolor='0.3'), size=7, alpha=0.8)

        #ax.set_xticks([ 0.5, 1.5, 2.5, 3.5,  4.5,  5.5, 6.5])

        major_ticks = np.arange(0.5, 7.5, 1)
        minor_ticks = np.arange(0, 7, 1)

        ax.set_xticks(major_ticks)
        ax.set_xticks(minor_ticks, minor=True)
        ax.set_yticks(major_ticks)
        ax.set_yticks(minor_ticks, minor=True)
        
        ax.set_xticklabels(["Strongly Disagree", "Disagree", 
                            "Mildly Disagree", "Neutral", "Mildly Agree", 
                            "Agree", "Fully Agree"], 
                            ha="left", rotation=45, size=8)
        
        ax.set_yticklabels(
            ["Strongly Disagree", "Disagree", 
             "Mildly Disagree", "Neutral", "Mildly Agree", 
             "Agree", "Fully Agree"],
            size=8, va="center")

        plt.xlabel("Opponent")
        plt.ylabel("Discussant")

        plt.title(f"Discussant {d} rate given Opponent stance")

        plt.tight_layout()
        if filename is not None:
            plt.savefig(filename)
            plt.clf()
        else:
            plt.show()
