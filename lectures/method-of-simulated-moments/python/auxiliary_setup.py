import os
import yaml
import pandas as pd
import matplotlib.pyplot as plt


def load_model_specs():
    ROOT = os.getcwd()
    os.chdir("../../configurations/robinson")

    options = yaml.safe_load(open("robinson.yaml", "r"))
    params_true = pd.read_csv(open("robinson.csv", "r"))
    params_true.set_index(["category", "name"], inplace=True)

    os.chdir(ROOT)

    return params_true, options


def format_plots():
    plt.style.use("../../configurations/matplotlibrc")
