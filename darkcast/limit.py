import os, sys, inspect, utils

###############################################################################
# Update the limit paths.
sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(
                inspect.getfile(inspect.currentframe()))), "limits"))
if os.getenv("DARKCAST_LIMIT_PATH"):
    for path in reversed(os.getenv("DARKCAST_LIMIT_PATH").split(":")):
        sys.path.insert(1, path)

###############################################################################
class LimitError(Exception):
    """
    Simple exception for the 'Limit' class.
    """
    pass

###############################################################################
class Limit:
    """
    Represents all the needed information to define a limit. This
    class contains the following members.
    
    notes:      text providing any relevant notes for the limit. This is
                optional, and if not defined a default will be assigned.
    bibtex:     the optional BibTex entry from inSPIRE for this limit.
    model:      the model defining the limit, must be of class 'Model'.
    production: production which contains the production mechanism or 
                mechanisms for the limit. Must be of class 'Production'.
    bounds:     the actual bounds for the limit. This can either be
                a 'Dataset' when a single-sided bound or 'Datasets' when
                a double-sided bound.
    efficiency: efficiency of class 'Efficiency'.
    """
    def __init__(self, name):
        """
        Initialize a limit, given its name.

        The limit must exist in the form <name>.py and is searched for
        along these paths in the following order:
        (0) The current directory within the Python interpreter.
        (1) The paths defined by the environment variable 
            'DARKCAST_LIMIT_PATH'.
        (2) The Darkcast package path.

        Each limit must have a model, production, decay, bounds, and
        efficiency defined. Optionally, notes and a BibTex entry can
        be provided.

        name: name of the limit.
        """
        self.name = name

        # Import the limit.
        limit = __import__(name)

        # Load the notes and BibTeX.
        try: self.notes = limit.notes
        except: self.notes = "The limit %s has no notes." % name
        try: self.bibtex = limit.bibtex
        except: self.bibtex = "The limit %s has no BibTeX entry." % name

        # Load the model.
        if not hasattr(limit, 'model'): raise LimitError(
            "No model is defined for '%s'." % name)
        self.model = limit.model
        self.model.width('total', 1)
        
        # Load the production.
        if not hasattr(limit, 'production'): raise LimitError(
            "No production is defined for '%s'." % name)
        self.production = limit.production
        self.production.ratio(1, 1, 1, self.model, self.model)

        # Load the decay.
        try: self.decay = limit.decay
        except: raise LimitError(
            "No decay is defined for '%s'." % name)
        try: self.model.width(self.decay, 1)
        except: raise LimitError(
            "The decay defined for '%s' is not valid." % name)

        # Load the bounds.
        if not hasattr(limit, 'production'): raise LimitError(
            "No bounds are defined for '%s'." % name)
        if not 'lower' in limit.bounds: self.bounds = {'lower': limit.bounds}
        else: self.bounds = limit.bounds
        for key, bound in self.bounds.items(): bound(1)

        # Load the efficiency.
        if not hasattr(limit, 'efficiency'): raise LimitError(
            "No efficiency is defined for '%s'." % name)
        self.efficiency = limit.efficiency
        self.efficiency.ratio(1, self, 1, 1)

    ###########################################################################
    def recast(self, model, gmax = 1e5):
        """
        Recast these limits to a given model. Returns a dictionary
        with entries of 'lower' and when relevant, 'upper'. Each entry
        is of the form: [[m0, m1, ...], [g0, g1, ...]].

        model: model for recasting, must be of type 'Model', e.g. 
               Model('dark_photon').
        gmax:  maximum coupling to recast. If a coupling is greater than 
               or equal to this, then that mass point is skipped.
        """
        # Initialize the recast bounds.
        lower0 = [[], []]
        upper0 = [[], []] if 'upper' in self.bounds else None
        lower1 = self.bounds['lower']

        # Loop over the masses.
        g0l = None
        for m in lower1.axes[0]:

            # Check if limit is above maximum and set guess.
            g1l = lower1(m)
            if g1l >= gmax: 
                lower0[0].append(m); lower0[1].append(gmax)
                if upper0: upper0[0].append(m); upper0[1].append(gmax)
                continue
            ggl = g0l if g0l != None else g1l

            # Check if branching fraction and production is non-zero.
            if model.bfrac(self.decay, m) == 0: continue
            if self.model.bfrac(self.decay, m) == 0: continue
            if self.production.ratio(m, 1, 1, model, self.model) == 0: continue

            # Solve equation 2.2 for the lower bound.
            f = lambda g: (
                model.bfrac(self.decay, m)/self.model.bfrac(self.decay, m)
                * self.production.ratio(m, g, g1l, model, self.model) 
                * self.efficiency.ratio(m, self, model.tau(m, g), 
                                        self.model.tau(m, g1l)) - 1)
            try: g0l = utils.solve(f, x = ggl)
            except: continue

            # If upper bound, find second zero, e.g. equations C.5 - C.7.
            if not upper0: lower0[0].append(m); lower0[1].append(g0l)
            else:
                if f(g0l*1.01) < 0:
                    try: g0u = utils.solve(f, x1 = g0l*0.99)
                    except: g0u = None
                else:
                    try: g0u = utils.solve(f, x0 = g0l*1.01)
                    except: g0u = None
                if g0u:
                    if g0u < g0l: g0u, g0l = g0l, g0u
                    lower0[0].append(m); lower0[1].append(g0l)
                    upper0[0].append(m); upper0[1].append(g0u)
        return {'lower': lower0, 'upper': upper0}
