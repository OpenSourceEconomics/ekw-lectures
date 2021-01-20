"""Auxiliary functions for introduction lecture."""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def plot_observed_choices(df):
    """Plot choices per period."""
    df["Age"] = df.index.get_level_values("Period") + 16
    df["Choice"].cat.categories = ["Blue", "White", "Schooling", "Home"]

    fig, ax = plt.subplots()

    labels = ["Home", "Schooling", "Blue", "White"]
    shares = df.groupby("Period").Choice.value_counts(normalize=True).unstack()[labels] * 100
    shares.plot.bar(stacked=True, ax=ax, width=0.8)

    ax.legend(labels=labels, loc="lower center", bbox_to_anchor=(0.5, 1.04), ncol=4)

    ax.yaxis.get_major_ticks()[0].set_visible(False)
    ax.set_ylabel("Share (in %)")
    ax.set_ylim(0, 100)

    ax.set_xticklabels(np.arange(16, 55, 5), rotation="horizontal")
    ax.xaxis.set_ticks(np.arange(0, 40, 5))


def plot_time_preference(deltas, edu_level):
    """Plot time preferences."""
    fig, ax = plt.subplots(1, 1)
    ax.fill_between(deltas, edu_level)

    ax.yaxis.get_major_ticks()[0].set_visible(False)
    ax.set_ylabel("Average final schooling")
    ax.set_ylim([10, 19])

    ax.set_xlabel(r"$\delta$")


def plot_policy_forecast(subsidies, edu_level):
    """Plot policy forecast."""
    fig, ax = plt.subplots(1, 1)
    ax.fill_between(subsidies, edu_level)

    ax.yaxis.get_major_ticks()[0].set_visible(False)
    ax.set_ylabel("Average final schooling")
    ax.set_ylim([10, 19])

    ax.xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter("{x:,.0f}"))
    ax.set_xlabel("Tuition subsidy")
    ax.set_xlim([None, 1600])
