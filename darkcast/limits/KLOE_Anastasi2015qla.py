from darkcast import pars, Model, Production, Dataset, Efficiency
notes = """
This limit was extracted from figure 9 (blue filled curve labeled
KLOE(3)) of Anastasi:2016ktq.

This is a prompt search with a flight distance less than 8 cm. The
production is e+ e- -> gamma X at a center-of-mass energy of the phi
meson, so the gamma factor is on the order of (m_phi^2 + m^2)/(2 m_phi m).
"""
bibtex = """
@article{Anastasi:2015qla,
 author         = "Anastasi, A. and others",
 title          = "{Limit on the production of a low-mass vector boson in
                   $\mathrm{e}^{+}\mathrm{e}^{-} \to \mathrm{U}\gamma$,
                   $\mathrm{U} \to \mathrm{e}^{+}\mathrm{e}^{-}$ with the
                   KLOE experiment}",
 journal        = "Phys. Lett.",
 volume         = "B750",
 year           = "2015",
 pages          = "633-637",
 doi            = "10.1016/j.physletb.2015.10.003",
 eprint         = "1509.00740",
 archivePrefix  = "arXiv",
 primaryClass   = "hep-ex",
 SLACcitation   = "%%CITATION = ARXIV:1509.00740;%%"
}
"""
model = Model("dark_photon")
production = Production("e_e")
decay = "e_e"
bounds = Dataset("KLOE_Anastasi2015qla.lmt")
efficiency = Efficiency(
    t0 = 0, t1 = lambda m: 0.08/((pars.mms["phi"]**2 + m**2)
                                 /(2*pars.mms["phi"]*m) * pars.c))
