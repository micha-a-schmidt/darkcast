import math, utils

###############################################################################
class EfficiencyError(Exception):
    """
    Simple exception for the 'Efficiency' class.
    """
    pass

###############################################################################
class Efficiency:
    """
    Provides the efficiency for a given experiment.
    """
    ###########################################################################
    def __init__(self, t0 = 0, t1 = None, lratio = None, rue = None):
        """
        Initialize an efficiency. The efficiency is defined in terms
        of a proper lifetime interval between t0 and t1 (seconds). For
        a prompt experiment, only the upper proper time needs to be
        provided, e.g. t1. For a displaced experiment, only 'lratio'
        (e.g. the ratio between the decay volume length and the shielding
        length, L_det/L_sh) needs to be provided, and t0 and t1 will
        be solved for using the lower and upper limits.

        t0:     value or function for the lower proper lifetime (seconds).
        t1:     value or function for the upper proper lifetime (seconds).
        lratio: ratio between the decay and shielding volume for a beam-dump
                experiment.
        """
        # Initialize the cached results.
        self.__cache = (None, None, None)

        # Set the lower proper time.
        if lratio > 0: self.__lratio = 1.0 + lratio
        else:
            try: t0 = float(t0); self.__t0 = lambda m: t0
            except: self.__t0 = t0
 
        # Set the upper proper time.
        if not lratio > 0:
            try: t1 = float(t1); self.__t1 = lambda m: t1
            except: self.__t1 = t1

    ###########################################################################
    def __ts(self, m, limit):
        """
        Return the proper time fiducial. If a displaced limit and
        'lratio' was specified, solve for t0 and t1.

        m:     mass (GeV).
        limit: 'Limit' which includes a model and lower/upper bounds.
        """
        # Fiducial from displaced limit.
        if self.__cache[0:-1] == (m, limit): return self.__cache[-1]
        try: lratio = self.__lratio
        except: lratio = None
        if lratio:

            # Solve t0 from equation 2.24.
            g0 = limit.bounds["lower"](m)
            g1 = limit.bounds["upper"](m)
            tau0 = limit.model.tau(m, g0)
            tau1 = limit.model.tau(m, g1)
            f = lambda t: (
                g1**2*(math.exp(-t/tau1) - math.exp(-t*self.__lratio/tau1))
                - g0**2*(math.exp(-t/tau0) - math.exp(-t*self.__lratio/tau0)))
            t0 = utils.solve(f)

            # Set t1 from equation 2.22.
            t1 = t0*self.__lratio

        # Fiducial from user defined proper times.
        else: t0, t1 = self.__t0(m), self.__t1(m)
        self.__cache = (m, limit, (t0, t1))
        return t0, t1

    ###########################################################################
    def ratio(self, m, limit, tau0, tau1):
        """
        Return the efficiency ratios for a given mass, limit, and
        lifetimes.
        
        m:     mass (GeV).
        limit: 'Limit' which includes a model and lower/upper bounds.
        tau0:  numerator lifetime (seconds).
        tau1:  denominator lifetime (seconds).
        """
        # Ratio of efficiencies, given by equation 2.23.
        t0, t1 = self.__ts(m, limit)
        return (math.exp(-t0/tau0) - math.exp(-t1/tau0))/(
            math.exp(-t0/tau1) - math.exp(-t1/tau1))
