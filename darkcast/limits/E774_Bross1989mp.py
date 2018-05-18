from darkcast import pars, Model, Production, Datasets, Efficiency
notes = """
This limit was extracted from figure 2 (orange dashed curve labeled
E774) of Andreas:2012mt.

This is a displaced search where the decay volume length over the
shielding length is 2/0.3.
"""
bibtex = """
@article{Bross:1989mp,
 author         = "Bross, A. and Crisler, M. and Pordes, Stephen H. and
                   Volk, J. and Errede, S. and Wrbanek, J.",
 title          = "{A Search for Short-lived Particles Produced in an
                   Electron Beam Dump}",
 journal        = "Phys. Rev. Lett.",
 volume         = "67",
 year           = "1991",
 pages          = "2942-2945",
 doi            = "10.1103/PhysRevLett.67.2942",
 reportNumber   = "FERMILAB-PUB-89-138-E",
 SLACcitation   = "%%CITATION = PRLTA,67,2942;%%"
}
"""
model = Model("dark_photon")
production = Production("e_brem")
decay = "e_e"
bounds = Datasets("E774_Bross1989mp.lmt")
efficiency = Efficiency(lratio = 2.0/0.3)
