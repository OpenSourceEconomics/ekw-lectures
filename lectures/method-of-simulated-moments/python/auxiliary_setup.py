import os

import matplotlib.pyplot as plt
import pandas as pd
import yaml


def load_model_specs():
    ROOT = os.getcwd()
    os.chdir("../../configurations/robinson")

    options = yaml.safe_load(open("robinson.yaml"))
    params_true = pd.read_csv(open("robinson.csv"))
    params_true.set_index(["category", "name"], inplace=True)

    os.chdir(ROOT)

    return params_true, options


def format_plots():
    plt.style.use("../../configurations/matplotlibrc")
