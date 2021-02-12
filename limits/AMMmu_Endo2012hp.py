# DARKCAST is licensed under the GNU GPL version 2 or later.
# Copyright (C) 2021 Philip Ilten, Yotam Soreq, Mike Williams, and Wei Xue.
import darkcast
notes = """
This limit is set from the difference between the measured muon
anomalous magnetic moment and SM prediction, and was calculated using
AMMe_Endo2012hp.py as a script, following the results of Endo:2012hp.

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
production = darkcast.Production("mu_mu")
decay = "none"
bounds = darkcast.Dataset("limits/AMMmu_Endo2012hp.lmt")
efficiency = darkcast.Efficiency(t0 = 0, t1 = float("inf"))
