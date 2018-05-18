import os, sys, inspect, math, pars

###############################################################################
# Update the model paths.
sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(
                inspect.getfile(inspect.currentframe()))), "models"))
if os.getenv("DARKCAST_MODEL_PATH"):
    for path in reversed(os.getenv("DARKCAST_MODEL_PATH").split(":")):
        sys.path.insert(1, path)

###############################################################################
class ModelError(Exception):
    """
    Simple exception for the 'Model' class.
    """
    pass

###############################################################################
class Model:
    """
    Provides the information and methods needed to define a given
    model, e.g. 'dark_photon'.

    name:   name of the model.
    xfs:    dictionary of fermion couplings.
    q:      quark U(3) charge matrix.
    states: allowed final states for the model, by default, all.
    """
    ###########################################################################
    def __init__(self, name):
        """
        Load a model, given its name.

        The model must exist in the form <name>.py and is searched for
        along these paths in the following order:
        (0) The current directory within the Python interpreter.
        (1) The paths defined by the environment variable 
            'DARKCAST_MODEL_PATH'.
        (2) The Darkcast package path.

        Each model must contain a fermion coupling dictionary named
        'xfs'.

        The list 'states' may be defined, specifying the allowed final
        states for the model, e.g. ['e_e', 'mu_mu', 'invisible',
        ...]. Only these final states are used when calculating the
        total width. If not defined, all visible and invisible final
        states are used when calculating the total width.

        Optionally, an 'iwidth' function provides the invisible width
        for the model, given a mass and model and taking the form
        'iwidth(mass (GeV), model)'. Consequently, the invisible width
        can be defined as a function of the visible width. If no
        'iwidth' is defined the invisible width is taken as zero. The
        invisible width is assumed to be dependent on the square of
        the global coupling. See the example model for further
        details.
        
        name: name of the model.
        """
        # Import the model.
        self.name = name
        self.__cache = (None, None, None)
        model = __import__(name)

        # Load the model's fermion couplings.
        self.xfs = {}
        for f in pars.mfs:
            try: self.xfs[f] = model.xfs[f]
            except: raise ModelError(
                "Error loading '%s' coupling from '%s'." % (f, name))

        # Load the model's invisible width function.
        try: self.__iwidth = model.iwidth
        except: self.__iwidth = lambda m, model: 0.0
        self.__iwidth(0, self)

        # Create the quark U(3) charge matrix.
        self.q = [self.xfs["u"], self.xfs["d"], self.xfs["s"]]

        # Load the model's defined final states.
        try: self.states = model.states
        except: self.states = ["visible", "invisible"]
        try: self.width("total", 0)
        except: raise ModelError(
            "Invalid definition of allowed final states from '%s'." % name)

    ###########################################################################
    def trq(self, t):
        """
        Return the trace of the quark U(3)-charge matrix for the model
        with the diagonal of a given matrix, e.g. a meson generator T.
        
        t: diagonal of the matrix to perform the trace with, must be
           size 3.
        """
        try:
            return t[0]*self.xfs["u"] + t[1]*self.xfs["d"] + t[2]*self.xfs["s"]
        except: raise ModelError(
            "Invalid diagonal provided to the trace.")

    ###########################################################################
    def width(self, states, m, g = 1.0):
        """
        Return the width, in 1/GeV, for the specified states, mass,
        and global coupling.

        states: final state or states.
        m:      mass (GeV).
        g:      global coupling (unitless).
        """
        # Return the cached results if valid.
        if self.__cache[0:-1] == (states, m): return g*g*self.__cache[-1]

        # Loop over the states.
        gamma = 0
        for state in (states,) if not hasattr(states, "__iter__") else states:
    
            # Invisible, visible, hadronic, and total widths.
            dtrs = state.split("_")
            if state == "invisible":
                gamma += self.__iwidth(self, m)
            elif state == "visible":
                gamma += self.width(
                    ["e_e", "mu_mu", "tau_tau", "nue_nue", "numu_numu", 
                     "nutau_nutau", "c_c", "b_b", "t_t", "hadrons"], m)
            elif state == "hadrons":
                gamma += self.width(pars.rfs.keys(), m)
            elif state == "total":
                gamma += self.width(self.states, m)
    
            # Perturbative decay into a fermion pair, equation 2.13.
            elif len(dtrs) == 2 and dtrs[0] == dtrs[1] and dtrs[0] in pars.mfs:
                dtr = dtrs[0]
                cf, mf, xf = pars.cfs[dtr], pars.mfs[dtr], self.xfs[dtr]
                if m > 2*mf:
                    gamma += (cf*xf**2.0*m/(12.0*math.pi)*(
                            1.0 + mf**2/m**2)*math.sqrt(1.0 - 4.0*mf**2.0/m**2))

            # Decay into hadrons, equations 2.17 and 2.18.
            elif state in pars.rfs:
                for mesons, rf in pars.rfs[state].items():
                    partial = 1
                    for meson in mesons:
                        partial *= pars.rvs[meson]*self.trq(pars.tms[meson])
                    partial *= partial if len(mesons) == 1 else 2
                    partial *= rf(m)
                    gamma += m/(12*math.pi)*partial

            else: raise ModelError(
                "Unknown state '%s'." % state)
        self.__cache = (states, m, gamma)
        return g*g*gamma

    ###########################################################################
    def tau(self, m, g = 1.0):
        """
        Return the lifetime, in seconds, for the specified mass and
        and global coupling.
        """
        return pars.hbar/self.width("total", m, g)

    ###########################################################################
    def bfrac(self, states, m):
        """
        Return the branching fraction for the specified states and mass.

        states: final state or states.
        m:      mass (GeV).
        """
        num = self.width(states, m)
        if num == 0: return 0.0
        den = self.width("total", m)
        if den == 0: return 0.0
        return num/den
