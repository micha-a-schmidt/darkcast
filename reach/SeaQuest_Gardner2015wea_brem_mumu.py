# DARKCAST is licensed under the GNU GPL version 2 or later.
# Copyright (C) 2018 Philip Ilten, Yotam Soreq, Mike Williams, and Wei Xue.
import darkcast
notes = """
This limit is a projection for SeaQuest searches using a di-muon
final state and produced from proton bremsstrahlung. This limit was
extracted from figure 2 (red hashed fills) of Gardner:2015wea.

This is a displaced search where the decay volume length over the
shielding length is 5/25.
"""
bibtex = """
@article{Gardner:2015wea,
 author         = "Gardner, S. and Holt, R. J. and Tadepalli, A. S.",
 title          = "{New Prospects in Fixed Target Searches for Dark Forces
                   with the SeaQuest Experiment at Fermilab}",
 journal        = "Phys. Rev.",
 volume         = "D93",
 year           = "2016",
 number         = "11",
 pages          = "115015",
 doi            = "10.1103/PhysRevD.93.115015",
 eprint         = "1509.00050",
 archivePrefix  = "arXiv",
 primaryClass   = "hep-ph",
 SLACcitation   = "%%CITATION = ARXIV:1509.00050;%%"
}
"""
model = darkcast.Model("dark_photon")
production = darkcast.Production("p_brem")
decay = "mu_mu"
bounds = darkcast.Datasets("reach/SeaQuest_Gardner2015wea_brem_mumu.lmt")
efficiency = darkcast.Efficiency(lratio = 5.0/25.0)
