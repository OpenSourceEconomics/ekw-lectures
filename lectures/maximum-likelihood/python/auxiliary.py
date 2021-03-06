"""Auxiliary function for maximum-likelihood lecture."""
import pickle as pkl

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_likelihood(rslts, params_base):
    """Plot likelihood function."""
    for index, fvals in rslts.items():
        fig, ax = plt.subplots()

        upper, lower = params_base.loc[index][["upper", "lower"]]
        grid = np.linspace(lower, upper, 20)

        ax.axvline(
            params_base.loc[index, "value"],
            color="#A9A9A9",
            linestyle="--",
            label="Baseline",
        )
        ax.plot(grid, np.array(fvals) / np.max(fvals))
        ax.set_title(index)
        plt.show()


def plot_score_function(norm_grid, norm_fds):
    """Plot score function."""
    fig, ax = plt.subplots()

    ax.set_title(r"$\delta$")

    ax.plot(norm_grid, norm_fds, label="gradient")
    ax.plot(norm_grid, norm_grid, label="benchmark")
    ax.legend()

    plt.show()


def plot_computational_budget(grid, rslts):
    """Plot computational budget example."""
    fig, ax = plt.subplots()

    ax.plot(grid, rslts)

    ax.set_ylabel("Seconds")
    ax.set_xlabel("Evaluation points")

    plt.show()


def plot_bootstrap_distribution():
    """Plot bootstrap distribution."""
    index = ("delta", "delta")
    for is_perturb in [True, False]:

        fname = f"material/bootstrap.delta_perturb_{str(is_perturb).lower()}.pkl"
        boot_params = pd.read_pickle(fname)

        fig, ax = plt.subplots()

        ax.hist(boot_params.loc[index, :], density=True)
        ax.set_title(f"{index}, perturbed {is_perturb}")
        ax.set_xlim(0.945, 0.955)

        plt.show()


def plot_score_distribution():
    """Plot score distribution."""
    rslts = pkl.load(open("material/score.delta.pkl", "rb"))

    fig, ax = plt.subplots()

    ax.hist(rslts, density=True)
    ax.set_title(r"$\delta$")


def plot_smoothing_parameter(rslts, params_base, grid):
    """Plot results for smoothing parameter."""
    fig, ax = plt.subplots()

    index = ("delta", "delta")

    ax.axvline(params_base.loc[index, "value"], color="#A9A9A9", linestyle="--")

    for tau, fvals in rslts.items():
        ax.plot(grid, fvals, label=f"{tau}")

    ax.set_title(r"$\delta$")
    ax.legend()
