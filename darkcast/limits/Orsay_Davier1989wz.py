from darkcast import pars, Model, Production, Datasets, Efficiency
notes = """
This limit was extracted from figure 2 (solid blue curve labeled
Orsay) of Andreas:2012mt.

This is a displaced search where the decay volume length over the
shielding length is 2/1.
"""
bibtex = """
@article{Davier:1989wz,
 author         = "Davier, M. and Nguyen Ngoc, H.",
 title          = "{An Unambiguous Search for a Light Higgs Boson}",
 journal        = "Phys. Lett.",
 volume         = "B229",
 year           = "1989",
 pages          = "150-155",
 doi            = "10.1016/0370-2693(89)90174-3",
 reportNumber   = "LAL 89-24",
 SLACcitation   = "%%CITATION = PHLTA,B229,150;%%"
}
"""
model = Model("dark_photon")
production = Production("e_brem")
decay = "e_e"
bounds = Datasets("Orsay_Davier1989wz.lmt")
efficiency = Efficiency(lratio = 2.0/1.0)
