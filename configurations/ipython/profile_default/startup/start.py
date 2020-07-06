from IPython import get_ipython

ipython = get_ipython()
ipython.magic("matplotlib inline")
ipython.magic("load_ext autoreload")
ipython.magic("autoreload 2")

import warnings
warnings.simplefilter(action="ignore", category=RuntimeWarning)