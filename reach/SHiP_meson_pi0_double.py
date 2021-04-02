# DARKCAST is licensed under the GNU GPL version 2 or later.
# Copyright (C) 2020 Philip Ilten, Yotam Soreq, Mike Williams, and Wei Xue.
import darkcast
notes = """ 
This limit is a projection for SHiP searches using secondary light meson
production. This limit was given by author of the paper.
"""
bibtex = """
@article{shipdp,
    archiveprefix = {arXiv},
    author = {SHiP Colloboration},
    eprint = {2011.05115},
    journal = {Submitted to EPJC},
    keywords = {ship, dp},
    title = {Sensitivity of the SHiP experiment to dark photons decaying to a pair of charged particles},
    year = {2020}}
"""
model = darkcast.Model("dark_photon")
production = darkcast.Production("pi0_gamma")
decay = "e_e"
efficiency = darkcast.Efficiency(lratio = 35.0/50.0)
