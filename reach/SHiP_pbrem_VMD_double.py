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
production = darkcast.Production("p_brem")
decay = ["e_e","mu_mu","pi+_pi-","pi+_pi-_pi0_pi0","pi+_pi-_pi0","pi+_pi-_pi+_pi-","K_K","K_K_pi","other"]
bounds = darkcast.Datasets("reach/SHiP_pbrem_VMD_double.lmt")
efficiency = darkcast.Efficiency(lratio = 35.0/50.0)
