"""Auxiliary functions for `hyperbolic_discounting.ipynb`."""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from dictionaries import color_dict
from dictionaries import label_dict
from dictionaries import policy_dict
from dictionaries import style_dict
from dictionaries import title_dict
from mpl_toolkits.axes_grid1.colorbar import colorbar


def compare_choice_probabilities(
    df, policy_dict=policy_dict, color_dict=color_dict, label_dict=label_dict
):
    """Plot choice probabilities, comparing behavior of restricted and unrestricted agents.

    Args:
        df (pd.DataFrame): Dataframe with choice probabilities.
        policy_dict (dict): Dictionary, from policies to labels.
        color_dict (dict): Dictionary, from choices to colors.
        label_dict (dict): Dictionary, from choices to labels.

    Return:
        Matplotlib figure.

    """
    fig = plt.figure(figsize=(15, 5))

    # policies
    policies = list(policy_dict.keys())
    n_policies = len(policies)

    # specify grid
    height_ratios = [1 / n_policies] * n_policies
    gs = fig.add_gridspec(n_policies, 2, height_ratios=height_ratios, width_ratios=[0.5, 1])

    # conditional choices axis
    axs = [fig.add_subplot(gs[i, 0]) for i in range(0, n_policies)]

    # unconditional choices axis
    ax_main = fig.add_subplot(gs[0:, 1:2])

    for ax, policy in zip(axs, policies):

        df.query("Policy == @policy").groupby("Period").Choice.value_counts(
            normalize=True
        ).unstack().plot.bar(stacked=True, rot=0, legend=False, width=1, color=color_dict, ax=ax)

        # decluttering
        ax.xaxis.label.set_visible(False)
        ax.yaxis.label.set_visible(False)
        ax.xaxis.set_ticks([])
        ax.yaxis.set_ticks([])

        # set policy name
        ax.set_title(policy_dict[policy], pad=20, x=-0.095, y=0, weight="bold", fontsize=16)

        # set dashed line at t = 4, where agents are restricted
        if policy == "restricted":
            ax.axvline(x=3.5, color="black", linestyle="dashed", linewidth=2)
        if policy == "veryrestricted":
            ax.axvline(x=3.5, color="black", linestyle="dashed", linewidth=2)
            ax.axvline(x=1.5, color="black", linestyle="dashed", linewidth=2)

    plt.suptitle("Conditional Choice Probabilities", x=0.255, y=1.07, fontsize=18, weight="bold")

    # main axis (unconditional choice probabilities)
    df.groupby("Period").Choice.value_counts(normalize=True).unstack().plot.bar(
        stacked=True,
        rot=90,
        legend=False,
        color=color_dict,
        width=1,
        ax=ax_main,
    )
    ax_main.yaxis.tick_right()
    ax_main.tick_params(right=False, bottom=False)
    ax_main.set_title("Unconditional Choice Probabilities", y=1.18, fontsize=18, weight="bold")
    ax_main.set_xlabel("Period", x=0.96, labelpad=20, fontsize=18)

    # legend
    labels = list(label_dict.values())
    plt.legend(
        loc="lower center",
        bbox_to_anchor=(0, -0.3),
        ncol=len(labels),
        labels=labels,
        frameon=False,
    )

    # annotate time preference parameter
    delta = df["Discount_Rate"][0][0]
    beta = df["Present_Bias"][0][0]
    plt.gcf().text(0.125, 0.915, f"δ = {delta}, β = {beta}", fontstyle="oblique", fontsize=18)

    fig.subplots_adjust(wspace=0.025, hspace=0.05)

    return fig


def plot_heatmap3d(df_heatmap):
    """Plot 3D heatmap."""
    # 3D Plotting
    fig = plt.figure(figsize=(25, 18))
    ax = plt.axes(projection="3d")
    fig.set_facecolor("white")
    ax.set_facecolor("white")

    # axes
    ax.w_xaxis.pane.fill = False
    ax.w_yaxis.pane.fill = False
    ax.w_zaxis.pane.fill = False
    ax.w_zaxis.grid(visible=False)

    # labels
    ax.yaxis.labelpad = 30
    ax.xaxis.labelpad = 50
    ax.zaxis.labelpad = 30

    ax.tick_params(axis="z", pad=15)
    ax.tick_params(axis="x", pad=20)

    # data
    df_pivot = df_heatmap.pivot_table(values="val", index="beta", columns="delta")

    # coordinates
    x = np.arange(0.944, 0.962, 0.002)
    y = np.arange(0.75, 1.05, 0.01)
    x, y = np.meshgrid(x, y)

    z = df_pivot.iloc[:, 11:].values
    ax.set_zticks([])

    # colormap
    colormap = get_custom_cmap()
    surf = ax.plot_surface(x, y, z, cmap=colormap)
    format_ = mpl.ticker.ScalarFormatter(useOffset=False, useMathText=True)
    format_.set_powerlimits((3, 3))
    colorbar(
        surf,
        ax=ax,
        shrink=0.7,
        aspect=10,
        ticks=[10_000] + list(np.linspace(20_000, 140_000, 7)),
        format=format_,
    )

    # labels' names
    ax.set_xlabel(r"$\delta$", fontsize=20, rotation=270)
    ax.set_ylabel(r"$\beta$", fontsize=20)
    ax.set_zlabel("Criterion", fontsize=20, rotation=360)
    ax.set_title("Heatmap criterion", weight="bold", fontsize=28, y=1.05)

    # disable automatic rotation
    ax.zaxis.set_rotate_label(False)

    ax.view_init(50, 10)

    return fig


def get_custom_cmap():
    """Generate custom cmap."""
    steps = [0, 0.05, 0.2, 0.5, 1]
    hexcolors = ["#444572", "#577590", "#43aa8b", "#f9c74f", "#FAE450"]
    colors = list(zip(steps, hexcolors))
    cmap = mpl.colors.LinearSegmentedColormap.from_list(name="custom_cmap", colors=colors)

    return cmap


def plot_counterfactual_predictions(
    data_dict,
    mom,
    ylabel,
    style_dict=style_dict,
    title_dict=title_dict,
):
    """Plot predicted effect of tuition subsidy in each period.

    Args:
        data_dict (dict): Dictionary of data.
        mom (str):  Moment to plot.
        ylabel (str): Label of y-axis.
        style_dict (dict): Dictionary to style plot elements.
        title_dict (dict): Dictionaries of titles.

    Returns:
        Matplotlib.axes

    """
    fig, ax = plt.subplots(figsize=(15, 7.5))

    for key, data in data_dict.items():

        data = data[mom]

        ax.plot(data["mean"], color="black", linewidth=2, label=" ", **style_dict[key]["line"])

        ax.fill_between(
            range(0, len(data["mean"])),
            np.add(data["mean"], data["std"]),
            np.subtract(data["mean"], data["std"]),
            label=title_dict[key],
            **style_dict[key]["fill"],
        )

    ax.set_ylabel(ylabel, labelpad=20)
    ax.set_xlabel("Period", labelpad=10)

    handles, labels = ax.get_legend_handles_labels()
    handles_positions = [[0, 1, 2], [3, 4, 5]]
    bbox_to_anchor = [(0.6, 0.3), (0.95, 0.3)]

    for i, title in enumerate(["Mean", "SD"]):
        kwargs = {"labelspacing": 0.725} if title == "Mean" else {"handletextpad": 5}
        legend = plt.legend(
            handles=[handles[j] for j in handles_positions[i]],
            ncol=1,
            bbox_to_anchor=bbox_to_anchor[i],
            title=title,
            title_fontsize=16,
            frameon=False,
            **kwargs,
        )
        legend._legend_box.align = "left"
        plt.gca().add_artist(legend)

    return fig
