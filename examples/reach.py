# DARKCAST is licensed under the GNU GPL version 2 or later.
# Copyright (C) 2018 Philip Ilten, Yotam Soreq, Mike Williams, and Wei Xue.

# This example plots every projected limit available in
# darkcast/reach. The matplotlib module is required.

# Update the system path to find the Darkcast module.
# This assumes that 'examples' is in 'darkcast/examples.'
import sys, os, inspect, itertools, glob
sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(
                inspect.getfile(inspect.currentframe()))), "../../"))

# Import the Darkcast module.
import darkcast

# Load the dark photon model.
model = darkcast.Model("dark_photon")

# Load all the available limits in darkcast/limits and DARKCAST_LIMIT_PATH.
limits = darkcast.Limits()

# Load all the available projected bounds.
bounds = glob.glob("../reach/*.lmt")

# Load matplotlib and initialize the plot.
import matplotlib.pyplot as pyplot
colors = ["red", "green", "blue", "orange", "magenta", "cyan", "gray"]
fig, ax = pyplot.subplots()
icolor, labels = itertools.cycle(colors), {}

# Loop over the limits.
for label, limit in limits.items():
    if limit.model.width('invisible', 1) != 0: continue
    recast = limit.recast(model)
    if pyplot:
        for x, y in recast.plots():
            ax.fill(x, y, alpha = 1, color = "gray")

# Loop over the bounds.
for bound in bounds:
    if "MESA" in bound: continue
    reach = darkcast.Datasets(bound)
    for x, y in reach.plots():
        label = os.path.basename(bound.split("_")[0])
        if not label in labels: c = next(icolor); labels[label] = c
        else: c = labels[label]; label = None
        ax.fill(x, y, label = label, alpha = 0.3, color = c)

# Save the plot.
if pyplot:
    legend = ax.legend(loc = "best", ncol = 2, fontsize = 10)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim([2e-3, 1e2])
    ax.set_ylim([1e-8, 1e1])
    ax.set_xlabel("mass [GeV]")
    ax.set_ylabel("g")
    ax.set_title(darkcast.utils.latex(model.name))
    darkcast.utils.logo()
    fig.savefig("reach.pdf")
