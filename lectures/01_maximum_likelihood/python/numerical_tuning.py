import pickle as pkl

import respy as rp
import numpy as np


GRID_DRAWS = [5, 16]
NUM_AGENTS = 100
TAU = 1e-8

rslts = dict()

params_base, options_base = rp.get_example_model("robinson", with_data=False)


for num_draws in GRID_DRAWS:

    index = ("delta", "delta")

    options = options_base.copy()
    options["estimation_draws"] = num_draws
    options["solution_draws"] = num_draws

    options["estimation_tau"] = TAU
    options["simulation_agents"] = NUM_AGENTS

    simulate = rp.get_simulate_func(params_base, options)
    df = simulate(params_base)

    crit_func = rp.get_crit_func(params_base, options, df)
    grid = np.linspace(0.948, 0.952, 20)

    fvals = list()
    for value in grid:
        params = params_base.copy()
        params.loc[index, "value"] = value
        fvals.append(crit_func(params))

    rslts[num_draws] = fvals - np.max(fvals)

pkl.dump(rslts, open("tuning.draws.pkl", "wb"))