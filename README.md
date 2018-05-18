Darkcast is the companion software package to the paper "Serendipity
in dark photon searches" and is a framework for recasting constraints
from dark photon searches into other models. This package is still
under initial development, and so currently only the curves from
figure 2 have been made available. These can be used to calculate the
hadronic width for a model as given by equation 2.17. Updates will
shortly be forthcoming.

## VMD

Currently 5 curves are provided, corresponding to the 4 curves of
figure 2, and the interference between the $`\omega`$ and
$`\rho`$-like contributions to the $`\pi^+ \pi^- \pi^0`$ final
state. All curves are given as a function of $`m`$ in GeV.

* `vmd/3pi-cross-term.txt`: $`\Re\big\{\mathcal{A}^{\phi}_{3\pi}(m)
  \left[f_{3\pi}(m) + \mathcal{A}^{\omega}_{3\pi}(m) \right]^*`$
* `vmd/gamma-like.txt`: $`\mathcal{R}_\mu^\gamma(m)`$
* `vmd/omega-like.txt`: $`\mathcal{R}_\mu^\omega(m)`$
* `vmd/phi-like.txt`: $`\mathcal{R}_\mu^\phi(m)`$
* `vmd/rho-like.txt`: $`\mathcal{R}_\mu^\rho(m)`$

## REFS

This directory contains a .tex and .bib file that provide easy access to
dark-sector references.

## DARKCAST

This contains an initial version of the recasting code in
Python. Further documentation is forthcoming.