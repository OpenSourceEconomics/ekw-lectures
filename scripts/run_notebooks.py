#!/usr/bin/env python
"""This module executes all notebooks. It serves the main purpose to ensure that all can be
executed and work proper independently."""
import subprocess as sp
import glob
import os

os.chdir(os.environ['PROJECT_ROOT'] + '/lectures')


for dir_ in glob.glob("*"):
    
    os.chdir(dir_)
    
    for notebook in sorted(glob.glob('*.ipynb')):
        print(notebook)
        cmd = ' jupyter nbconvert --execute {}  --ExecutePreprocessor.timeout=-1'.format(notebook)
        sp.check_call(cmd, shell=True)

    os.chdir("../")
                      
    
