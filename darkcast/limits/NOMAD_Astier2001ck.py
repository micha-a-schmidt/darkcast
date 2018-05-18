from darkcast import pars, Model, Production, Datasets, Efficiency
notes = """
This limit was extracted from figure 5 (solid gray curve labeled NOMAD
& PS191 just below the nu-Cal I (pi0) line) of Blumlein:2013cua.

This is a displaced search where the decay volume length over the
shielding length is 7.5/835.
"""
bibtex = """
@article{Astier:2001ck,
 author         = "Astier, P. and others",
 title          = "{Search for heavy neutrinos mixing with tau neutrinos}",
 collaboration  = "NOMAD",
 journal        = "Phys. Lett.",
 volume         = "B506",
 year           = "2001",
 pages          = "27-38",
 doi            = "10.1016/S0370-2693(01)00362-8",
 eprint         = "hep-ex/0101041",
 archivePrefix  = "arXiv",
 primaryClass   = "hep-ex",
 reportNumber   = "CERN-EP-2001-005",
 SLACcitation   = "%%CITATION = HEP-EX/0101041;%%"
}
"""
model = Model("dark_photon")
production = Production("pi0_gamma")
decay = "e_e"
bounds = Datasets("NOMAD_Astier2001ck.lmt")
efficiency = Efficiency(lratio = 7.5/835.0)
