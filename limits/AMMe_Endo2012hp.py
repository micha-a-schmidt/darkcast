# DARKCAST is licensed under the GNU GPL version 2 or later.
# Copyright (C) 2021 Philip Ilten, Yotam Soreq, Mike Williams, and Wei Xue.
import darkcast
notes = """
This limit is set from the difference between the measured
electron anomalous magnetic moment and SM prediction, and was
calculated using this file as a script, following the results of
Endo:2012hp.

Given the nature of the limit, the efficiency ratio is unity, e.g. t0
= 0 and t1 = infinity.
"""
bibtex = """
@article{Endo:2012hp,
 author = "Endo, Motoi and Hamaguchi, Koichi and Mishima, Go",
 title = "{Constraints on Hidden Photon Models from Electron g-2 and 
          Hydrogen Spectroscopy}",
 eprint = "1209.2558",
 archivePrefix = "arXiv",
 primaryClass = "hep-ph",
 reportNumber = "UT-12-31, IPMU12-172",
 doi = "10.1103/PhysRevD.86.095029",
 journal = "Phys. Rev. D",
 volume = "86",
 pages = "095029",
 year = "2012"
}
"""
model = darkcast.Model("dark_photon")
production = darkcast.Production("e_e")
decay = "none"
try: bounds = darkcast.Dataset("limits/AMMe_Endo2012hp.lmt")
except: pass
efficiency = darkcast.Efficiency(t0 = 0, t1 = float("inf"))

###############################################################################
def epsilon(da, a0, ml, m):
    """
    Calculate the limit on epsilon for a given difference between
    a(observed) - a(SM theory). Based on equation 6 of
    Endo:2012hp. The fine structure contribution is not included as it
    is negligible.

    da: difference in anomalous magnetic moment, a(experiment) - a(SM).
    a0: fine structure constant.
    ml: mass of the lepton.
    m:  mass of the dark photon.
    """
    from scipy import integrate
    from math import pi
    loop = lambda z, ml=ml, m=m: (2*z*(1 - z)**2*ml**2)/(
        z*m**2 + (1 - z)**2*ml**2)
    return (da/(a0/(2*pi)*integrate.quad(loop, 0, 1)[0]))**0.5

###############################################################################
if __name__ == "__main__":
    """
    Calculate the limits file.
    """
    from darkcast import pars
    from math import log10
    import numpy
    a0 = 1/137.03599904

    # Electron AMM.
    da = 1.06e-12
    frm = "%11.4e"
    out = file("AMMe_Endo2012hp.lmt", "w")
    ttl = "#%%%is %%%is\n" % (len(frm % 1.0) - 1, len(frm % 1.0))
    out.write(ttl % ("mass", "lower"))
    for m in numpy.logspace(log10(1e-3), log10(1e2), 100):
        out.write((frm + " " + frm + "\n") %
                  (m, epsilon(da, a0, pars.mfs["e"], m)))
    out.close()

    # Muon AMM.
    da = 2.61e-9
    frm = "%11.4e"
    out = file("AMMmu_Endo2012hp.lmt", "w")
    ttl = "#%%%is %%%is\n" % (len(frm % 1.0) - 1, len(frm % 1.0))
    out.write(ttl % ("mass", "lower"))
    for m in numpy.logspace(log10(1e-3), log10(1e2), 100):
        out.write((frm + " " + frm + "\n") %
                  (m, epsilon(da, a0, pars.mfs["mu"], m)))
    out.close()
