
respy - lectures
================

This repository contains several lectures that use the ``respy`` package. These support our educational activities around our group's research code.

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
  :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
  :target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/badge/zulip-join_chat-brightgreen.svg
  :target: https://ose.zulipchat.com

Overview
--------

`Introduction to structural econometrics <https://nbviewer.jupyter.org/github/OpenSourceEconomics/respy-lectures/blob/master/lectures/introduction/notebook.ipynb>`_

We discuss the basic motivation behind structural econometric modeling. We quickly focus on the class of Eckstein-Keane-Wolpin models that are often used in labor economics to study human capital accumulation and discuss their economic model, mathematical formulation, and alternative calibration procedures. We explore the seminal work outlined in Keane & Wolpin (1994) as an example.

Calibration
-----------

**`Maximum likelihood estimation <https://nbviewer.jupyter.org/github/OpenSourceEconomics/respy-lectures/blob/master/lectures/maximum-likelihood/notebook.ipynb>`_**

We estimate the `Robinson Crusoe <https://nbviewer.jupyter.org/github/OpenSourceEconomics/respy-lectures/blob/master/lectures/robinson-economy/notebook.ipynb>`_ model using the method of maximum likelihood. We study the likelihood function, the distribution of the score statistic, linearity of the score function, and compare alternative methods to compute confidence intervals. Finally, we study the sensitivity of the likelihood function to numerical parameters.

`Method of simulated moments <https://nbviewer.jupyter.org/github/OpenSourceEconomics/respy-lectures/blob/master/lectures/method-of-simulated-moments/notebook.ipynb>`_

We estimate the `Robinson Crusoe <https://nbviewer.jupyter.org/github/OpenSourceEconomics/respy-lectures/blob/master/lectures/robinson-economy/notebook.ipynb>`_ model using the method of simulated moments. We revisit the basic ideas behind this approach and then prototype a criterion function and a weighting matrix. We conclude with  a Monte Carlo exploration of selected challenges in the estimation procedure.

Extensions
----------

We showcase several extensions to the baseline model and its standard analysis.

`Hyperbolic discounting <https://media.giphy.com/media/kHfUyPaDUDBY11l4DZ/giphy.gif>`_

... work in progress

`Robust decision-making <https://media.giphy.com/media/kHfUyPaDUDBY11l4DZ/giphy.gif>`_

... work in progress

`Uncertainty quantification <https://media.giphy.com/media/kHfUyPaDUDBY11l4DZ/giphy.gif>`_

... work in progress

Miscellaneous
-------------

`Robinson Crusoe model <https://nbviewer.jupyter.org/github/OpenSourceEconomics/respy-lectures/blob/master/lectures/robinson-economy/notebook.ipynb>`_

We outline the model that serves as the running example throughout the lectures.

Replications
------------

Please see ``respy``'s `online documentation <https://respy.readthedocs.io>`_ for several replications of seminal papers in the literature.

Powered by
----------

.. image:: docs/_static/images/OSE_sb_web.svg
  :width: 22 %
  :target: https://open-econ.org

.. image:: docs/_static/images/nuvolos_sidebar_logo_acblue.svg
  :width: 8 %
  :target: https://nuvolos.cloud
