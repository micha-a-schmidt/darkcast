# DARKCAST is licensed under the GNU GPL version 2 or later.
# Copyright (C) 2018 Philip Ilten, Yotam Soreq, Mike Williams, and Wei Xue.

# This example recasts every visible limit available in
# darkcast/limits to every model available in darkcast/models. If
# matplotlib is available these limits are then plotted. The produced
# figures correspond to figures 4 through 7 of Ilten:2018crw.

# Update the system path to find the Darkcast module.
# This assumes that 'examples' is in 'darkcast/examples.'
import sys, os, inspect, itertools
sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(
                inspect.getfile(inspect.currentframe()))), "../../"))

# Import the Darkcast module.
import darkcast

# Load all the available models in darkcast/models and DARKCAST_MODEL_PATH.
models = darkcast.Models()

# Load all the available limits in darkcast/limits and DARKCAST_LIMIT_PATH.
limits = darkcast.Limits()

# Alternatively, all the limits from a folder, '/foo/bar', could be
# loaded as:
#
# limits = darkcast.Limits("/foo/bar")
#
# Note that any limits in the directory that are not valid will not be
# loaded. A single limit with name 'foo_bar' can be loaded as:
#
# limit = darkcast.Limit("foo_bar")

# Try to load matplotlib.
try: import matplotlib.pyplot as pyplot
except: pyplot = None
colors = ["red", "green", "blue", "orange", "cyan", "magenta", "sienna", 
          "purple", "maroon", "navy", "gray"]

# Loop over all the models.
for name, model in models.items():
    print "Recasting limits to the %s model." % name

    # If possible, initialize the plot.
    if pyplot:
        fig, ax = pyplot.subplots()
        icolor, labels = itertools.cycle(colors), {}
        
    # Loop over the limits.
    for label, limit in limits.items():
        if limit.model.width('invisible', 1) != 0: continue
        else: print label
        
        # Recast the limit, this returns an object of type 'Datasets'.
        recast = limit.recast(model)

        # Save the limit to a text file. This is done with the
        # 'Datasets.write' method.
        recast.write("visible_%s_%s.txt" % (name, label))
            
        # Plot. The 'Datasets.plots' method returns formatted lists of
        # x and y points which can be easily passed to a plotting
        # package.
        if pyplot:
            label = label.split("_")[0]
            if not label in labels: color = next(icolor); labels[label] = color
            else: color = labels[label]; label = None
            for x, y in recast.plots():
                ax.fill(x, y, label = label, alpha = 0.3, color = color)
                label = None

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
        fig.savefig("visible_%s.pdf" % name)