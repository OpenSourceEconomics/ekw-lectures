================
Replication code
================

This is the code to generate the files in `hyperbolic_discounting/data`.

It uses the template by Hans-Martin von Gaudecker (see
`here <https://econ-project-templates.readthedocs.io/en/stable/>`_ for more information),
therefore it is fully and automatically reproducible conditional on having
`conda <https://docs.conda.io/en/latest/>`_ installed.

<hr />

To reproduce, first navigate to the root of the project (the `replication_code` folder).
Then, open your terminal emulator and run, line by line:

.. code-block:: zsh

    $ conda env create -f environment.yml
    $ conda activate hyperbolic_discounting
    $ python waf.py configure
    $ python waf.py build

The files will be in `bld/out/analysis`.
