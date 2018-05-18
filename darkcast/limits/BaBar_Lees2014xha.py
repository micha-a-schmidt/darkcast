from darkcast import pars, Model, Production, Dataset, Efficiency
notes = """
This limit was extracted from figure 4 (green curve labeled BaBar) of
Lees:2014xha. In this limit both the electron and muon final states
were combined; the associated supplemental material to Lees:2014xha
provides the cross-section limits for each final state.

This search is prompt, and is not sensitive to X bosons with lifetimes
large enough to qualify as non-prompt; the efficiency ratio is assumed
to be unity, e.g. t0 = 0 and t1 = infinity.
"""
bibtex = """
@article{Lees:2014xha,
 author         = "Lees, J. P. and others",
 title          = "{Search for a Dark Photon in $e^+e^-$ Collisions at
                   BaBar}",
 collaboration  = "BaBar",
 journal        = "Phys. Rev. Lett.",
 volume         = "113",
 year           = "2014",
 number         = "20",
 pages          = "201801",
 doi            = "10.1103/PhysRevLett.113.201801",
 eprint         = "1406.2980",
 archivePrefix  = "arXiv",
 primaryClass   = "hep-ex",
 reportNumber   = "BABAR-PUB-14-002, SLAC-PUB-15979",
 SLACcitation   = "%%CITATION = ARXIV:1406.2980;%%"
}
"""
model = Model("dark_photon")
production = Production("e_e")
decay = ["e_e", "mu_mu"]
bounds = Dataset("BaBar_Lees2014xha.lmt")
efficiency = Efficiency(t0 = 0, t1 = float("inf"))
