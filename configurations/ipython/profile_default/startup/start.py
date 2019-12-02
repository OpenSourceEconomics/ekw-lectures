from IPython.display import Image
from IPython import get_ipython

ipython = get_ipython()
ipython.magic('matplotlib inline')
ipython.magic('load_ext autoreload')
ipython.magic('autoreload 2')

from functools import partial
from pathlib import Path
import subprocess as sp
import pickle as pkl
import warnings
import shutil
import yaml
import os

import matplotlib.pyplot as plt
import seaborn as sns
import pickle as pkl
import pandas as pd
