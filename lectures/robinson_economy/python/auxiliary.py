import matplotlib.pyplot as plt


def plot_choice_probabilities(df):
    fig, ax = plt.subplots()

    df.groupby("Period").Choice.value_counts(normalize=True).unstack().plot.bar(
        stacked=True, ax=ax
    )

    plt.xticks(rotation="horizontal")

    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.275), ncol=2)
    ax.set_ylabel("Share")


def plot_distibution_wages(df):

    for period in df.index.get_level_values("Period").unique():

        fig, ax = plt.subplots()
        ax.hist(df.xs(period, level="Period")["Wage"], density=True)
        ax.set_title(f"Period {period}")
        ax.set_xlabel("Wage")


def plot_average_wages_over_time(df):

    fig, ax = plt.subplots()
    ax.plot(df.groupby("Period")["Wage"].mean())
    ax.set_xlabel("Period")
