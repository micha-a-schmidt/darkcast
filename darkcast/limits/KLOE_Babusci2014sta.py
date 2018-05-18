from darkcast import pars, Model, Production, Dataset, Efficiency
notes = """
This limit was extracted from figure 9 (blue filled curve labeled
KLOE(2)) of Anastasi:2016ktq.

This is a prompt search with a flight distance less than 8 cm. The
production is e+ e- -> gamma X at a center-of-mass energy of the phi
meson, so the gamma factor is on the order of (m_phi^2 + m^2)/(2 m_phi m).
"""
bibtex = """
@article{Babusci:2014sta,
 author         = "Babusci, D. and others",
 title          = "{Search for light vector boson production in $e^+e^-
                   \rightarrow \mu^+ \mu^- \gamma$ interactions with the KLOE
                   experiment}",
 collaboration  = "KLOE-2",
 journal        = "Phys. Lett.",
 volume         = "B736",
 year           = "2014",
 pages          = "459-464",
 doi            = "10.1016/j.physletb.2014.08.005",
 eprint         = "1404.7772",
 archivePrefix  = "arXiv",
 primaryClass   = "hep-ex",
 SLACcitation   = "%%CITATION = ARXIV:1404.7772;%%"
}
"""
model = Model("dark_photon")
production = Production("e_e")
decay = "mu_mu"
bounds = Dataset('KLOE_Babusci2014sta.lmt')
efficiency = Efficiency(
    t1 = lambda m: 0.08/((pars.mms["phi"]**2 + m**2)
                         /(2*pars.mms["phi"]*m) * pars.c))
