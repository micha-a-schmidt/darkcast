# DARKCAST is licensed under the GNU GPL version 2 or later.
# Copyright (C) 2019 Philip Ilten, Yotam Soreq, Mike Williams, and Wei Xue.
import darkcast
notes = """
This limit was extracted from figure 2 (red dashed curve labeled
E137) of Andreas:2012mt.

This is a displaced search where the decay volume length over the
shielding length is 204/179.
"""
bibtex = """
@article{Bjorken:1988as,
 author         = "Bjorken, J. D. and Ecklund, S. and Nelson, W. R. and
                   Abashian, A. and Church, C. and Lu, B. and Mo, L. W. and
                   Nunamaker, T. A. and Rassmann, P.",
 title          = "{Search for Neutral Metastable Penetrating Particles
                   Produced in the SLAC Beam Dump}",
 journal        = "Phys. Rev.",
 volume         = "D38",
 year           = "1988",
 pages          = "3375",
 doi            = "10.1103/PhysRevD.38.3375",
 reportNumber   = "FERMILAB-PUB-88-044, PRINT-88-0352 (FERMILAB)",
 SLACcitation   = "%%CITATION = PHRVA,D38,3375;%%"
}
"""
model = darkcast.Model("dark_photon")
production = darkcast.Production("e_brem")
decay = "e_e"
bounds = darkcast.Datasets("limits/E137_Bjorken1988as.lmt")
efficiency = darkcast.Efficiency(lratio = 204.0/179.0)
