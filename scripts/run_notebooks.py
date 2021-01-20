#!/usr/bin/env python
"""This module executes all notebooks.

It serves the main purpose to ensure that all can be executed and work proper
independently.
"""
import glob
import os
import subprocess as sp

os.chdir(os.environ["PROJECT_ROOT"] + "/lectures")
dir_list = glob.glob("*-*")
dir_list.append("introduction")

for dir_ in dir_list:

    os.chdir(dir_)

    for notebook in sorted(glob.glob("*.ipynb")):
        cmd = " jupyter nbconvert --to html --execute {}  --ExecutePreprocessor.timeout=-1".format(
            notebook
        )
        sp.check_call(cmd, shell=True)

    os.chdir("../")
