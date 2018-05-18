from darkcast import pars, Model, Production, Datasets, Efficiency
notes = """
This limit was extracted from figure 2 (purple dotted curve labeled
E141) of Andreas:2012mt.

This is a displaced search where the decay volume length over the
shielding length is 35/0.12.
"""
bibtex = """
@article{Riordan:1987aw,
 author         = "Riordan, E. M. and others",
 title          = "{A Search for Short Lived Axions in an Electron Beam Dump
                   Experiment}",
 journal        = "Phys. Rev. Lett.",
 volume         = "59",
 year           = "1987",
 pages          = "755",
 doi            = "10.1103/PhysRevLett.59.755",
 reportNumber   = "SLAC-PUB-4280, UR-993, FERMILAB-PUB-87-251",
 SLACcitation   = "%%CITATION = PRLTA,59,755;%%"
}
"""
model = Model("dark_photon")
production = Production("e_brem")
decay = "e_e"
bounds = Datasets("E141_Riordan1987aw.lmt")
efficiency = Efficiency(lratio = 35.0/0.12)
