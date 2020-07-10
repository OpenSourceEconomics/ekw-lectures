################
respy - lectures
################

This repository contains several lectures that use the ``respy`` package. These support our educational activities around our group's research code.

.. image:: https://github.com/luward/respy-lectures/workflows/Continuous%20Integration/badge.svg
  :target: https://github.com/luward/respy-lectures/actions

.. image:: _static/images/code-style-black.svg
  :target: https://github.com/psf/black

.. image:: _static/images/License-MIT-yellow.svg
  :target: https://opensource.org/licenses/MIT

.. image:: _static/images/zulip.svg
  :target: https://ose.zulipchat.com

=========
Overview
=========

.. toctree::
   :maxdepth: 1

   introduction/notebook.ipynb

We discuss the basic motivation behind structural econometric modeling. We quickly focus on the class of Eckstein-Keane-Wolpin models that are often used in labor economics to study human capital accumulation and discuss their economic model, mathematical formulation, and alternative calibration procedures. We explore the seminal work outlined in Keane & Wolpin (1994) as an example.

============
Calibration
============

.. toctree::
   :maxdepth: 1

   introduction/notebook.ipynb
   maximum-likelihood/notebook.ipynb

We estimate the Robinson Crusoe model using the method of maximum likelihood. We study the likelihood function, the distribution of the score statistic, linearity of the score function, and compare alternative methods to compute confidence intervals. Finally, we study the sensitivity of the likelihood function to numerical parameters.

.. toctree::
   :maxdepth: 1

   method-of-simulated-moments/notebook.ipynb

We estimate the Robinson Crusoe model using the method of simulated moments. We revisit the basic ideas behind this approach and then prototype a criterion function and a weighting matrix. We conclude with  a Monte Carlo exploration of selected challenges in the estimation procedure.

==========
Extensions
==========

We showcase several extensions to the baseline model and its standard analysis.

`Hyperbolic discounting <https://media.giphy.com/media/kHfUyPaDUDBY11l4DZ/giphy.gif>`_

... work in progress

`Robust decision-making <https://media.giphy.com/media/kHfUyPaDUDBY11l4DZ/giphy.gif>`_

... work in progress

`Uncertainty quantification <https://media.giphy.com/media/kHfUyPaDUDBY11l4DZ/giphy.gif>`_

... work in progress

=============
Miscellaneous
=============


.. toctree::
   :maxdepth: 1

   robinson-economy/notebook.ipynb

We outline the model that serves as the running example throughout the lectures.

============
Replications
============

Please see ``respy``'s `online documentation <https://respy.readthedocs.io>`_ for several replications of seminal papers in the literature.

==========
Powered by
==========

.. image:: _static/images/OSE_sb_web.svg
  :width: 22 %
  :target: https://open-econ.org

.. image:: _static/images/nuvolos_sidebar_logo_acblue.svg
  :width: 8 %
  :target: https://nuvolos.cloud

