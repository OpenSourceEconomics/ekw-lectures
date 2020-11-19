import pandas as pd
import respy as rp
import numpy as np


GRID_TAU = [0.01, 0.001, 0.0001, 0.00001, 0.000001, 0.0000001]
GRID_AGENTS = [100, 1000, 10000]
GRID_DRAWS = [100, 1000, 10000]


index = list()
for num_agents in GRID_AGENTS:
    for num_draws in GRID_DRAWS:
        for tau in GRID_TAU:
            index.append((num_agents, num_draws, tau))
index = pd.MultiIndex.from_tuples(index, names=("agents", "draws", "tau"))
rslts = pd.DataFrame(index=index, columns=["delta"])

params_base, options_base = rp.get_example_model("robinson", False)
delta_true = params_base.loc[("delta", "delta"), "value"]

for num_agents in GRID_AGENTS:

    options = options_base.copy()

    options["estimation_draws"] = num_draws
    options["solution_draws"] = num_draws

    for num_draws in GRID_DRAWS:

        simulate = rp.get_simulate_func(params_base, options)
        df = simulate(params_base)

        for tau in GRID_TAU:

            options["estimation_tau"] = tau
            options["simulation_agents"] = num_agents

            crit_func = rp.get_log_like_func(params_base, options, df)
            grid = np.concatenate((np.linspace(0.948, 0.952, 40), [delta_true]))

            fvals = list()
            for value in grid:
                params = params_base.copy()
                params.loc[("delta", "delta"), "value"] = value
                fvals.append(crit_func(params))

            rslts.loc[(num_agents, num_draws, tau), "delta"] = grid[fvals.index(max(fvals))]
            rslts.to_pickle("tuning.delta.pkl")
