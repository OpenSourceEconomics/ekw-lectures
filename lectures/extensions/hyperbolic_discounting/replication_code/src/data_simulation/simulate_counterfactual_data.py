"""Get counterfactual prediction for 2000 US dollars tuition subsidy.

Get counterfactual prediction for 2000 US dollars tuition subsidy for
different parametrization of the model with hyperbolic discounting and choice
restrictions based on Keane and Wolpin (1994) :cite:`KeaneWolpin1994`.

Looking at the bivariate distribution of the time preference parameters, it
seems that many combinations of beta (present bias) and delta (discount factor)
are compatible with the empirical data.
Therefore, I study the extent to which the counteractual predictions of these
competing parametrizations differ.

"""
import numpy as np
import pandas as pd
import respy as rp
from bld.project_paths import project_paths_join as ppj
from src.library.housekeeping import _save_to_pickle
from src.library.housekeeping import _temporary_working_directory
from tqdm import tqdm


def simulate_life_cycle_data(params, options):
    """Generate simulated life-cycle data (100 DataFrame).

    Args:
        params (pd.DataFrame): DataFrame containing model parameters.
        options (dict): Dictionary containing model options.

    Returns:
        List of pd.DataFrames.

    """
    params_ = params.copy()
    options_ = options.copy()

    n_datasets = 100
    sim_seeds = np.linspace(0, 99, n_datasets)
    sol_seeds = np.linspace(1000, 1099, n_datasets)

    col_to_keep = [
        "Experience_A",
        "Experience_B",
        "Experience_Edu",
        "Present_Bias",
        "Discount_Rate",
        "Choice",
        "Wage",
    ]

    # generate datasets
    list_of_results = [
        simulate_life_cycle_df(params_, options_, sim_seed, sol_seed, col_to_keep)
        for sim_seed, sol_seed in tqdm(zip(sim_seeds, sol_seeds))
    ]

    return list_of_results


def simulate_life_cycle_df(params, options, sim_seed, sol_seed, col_to_keep):
    """Simulate life cycle dataset, store choices and wages (mean and std).

    Args:
        params (pd.DataFrame): DataFrame containing model parameters.
        options (dict): Dictionary containing model options.
        sim_seed (int): Seed for simulation.
        sim_seed (int): Seed for solution.
        col_to_keep (list): Columns of the simulate data from which to compute
            relevant moments (choice and wages).

    Returns:
        pd.DataFrame.

    """
    with _temporary_working_directory(snippet=f"{sim_seed}_{sol_seed}"):
        options["simulation_seed"] = int(sim_seed)
        options["solution_seed"] = int(sol_seed)
        simulate = rp.get_simulate_func(params, options)
        df = simulate(params)

        # extract choices
        choices = df.groupby("Period").Choice.value_counts(normalize=True).unstack()

        # extract wages (mean and std)
        wages = df[col_to_keep].groupby("Period").describe().loc[:, (slice(None), ["mean", "std"])]
        res = pd.concat([wages, choices], axis=1)

    return res


if __name__ == "__main__":

    # load params
    params, options = rp.get_example_model("kw_94_three", with_data=False)
    options["simulation_agents"] = 10_000

    params_dict = {
        "true": {"delta": 0.95, "beta": 0.8},
        "miss_exp": {"delta": 0.938, "beta": 1},
        "miss_1": {"delta": 0.948, "beta": 0.83},
    }

    for model, time_params in params_dict.items():

        # no tuition subsidy
        params.loc[("delta", "delta"), "value"] = time_params["delta"]
        params.loc[("beta", "beta"), "value"] = time_params["beta"]

        data = simulate_life_cycle_data(params, options)
        _save_to_pickle(data, ppj("OUT_DATA", "counterfactual_data", f"data_{model}.pickle"))

        # delete saved data to free up memory
        del data

        # with tuition subsidy
        params_ = params.copy()
        params_.loc[("nonpec_edu", "at_least_twelve_exp_edu"), "value"] += 2_000

        data_subsidy = simulate_life_cycle_data(params_, options)
        _save_to_pickle(
            data_subsidy,
            ppj("OUT_DATA", "counterfactual_data", f"data_{model}_subsidy.pickle"),
        )

        # delete saved data to free up memory
        del data_subsidy
