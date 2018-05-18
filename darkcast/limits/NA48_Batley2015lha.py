from darkcast import pars, Model, Production, Dataset, Efficiency
notes = """
This limit was extracted from figure 4 (red filled curve labeled
NA48/2) of the associated paper, Batley:2015lha.

This is a prompt search, t0 = 0, with the flight distance less than 1
m. The production is from pi0 -> gamma X where the maximum energy of
the X-boson is 50 GeV (see text preceding equation 9), and so the
gamma factor is taken as 50/m.
"""
bibtex = """
@article{Batley:2015lha,
      author         = "Batley, J. R. and others",
      title          = "{Search for the dark photon in $\pi^0$ decays}",
      collaboration  = "NA48/2",
      journal        = "Phys. Lett.",
      volume         = "B746",
      year           = "2015",
      pages          = "178-185",
      doi            = "10.1016/j.physletb.2015.04.068",
      eprint         = "1504.00607",
      archivePrefix  = "arXiv",
      primaryClass   = "hep-ex",
      reportNumber   = "CERN-PH-EP-2015-093",
      SLACcitation   = "%%CITATION = ARXIV:1504.00607;%%"
}
"""
model = Model("dark_photon")
production = Production("pi0_gamma")
decay = "e_e"
bounds = Dataset("NA48_Batley2015lha.lmt")
efficiency = Efficiency(t0 = 0, t1 = lambda m: 1.0/(50.0/m * pars.c))
