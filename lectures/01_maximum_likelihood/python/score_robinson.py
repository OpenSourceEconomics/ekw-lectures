from functools import partial

from scipy.optimize import approx_fprime
import pickle as pkl
import respy as rp
import numpy as np


INDICES = [("delta", "delta")]
NUM_SIMULATIONS = 10000
NUM_DRAWS = 1000

EPS = np.sqrt(np.finfo(float).eps)


def wrapper_crit_func(crit_func, params_base, index, values):
    if isinstance(values, float):
        values = [values]

    params = params_base.copy()

    fvals = list()
    for value in values:
        params.loc[index, "value"] = value
        fvals.append(crit_func(params))

    if len(fvals) == 1:
        fvals = fvals[0]

    return fvals


params_base, options_base, df = rp.get_example_model("robinson", with_data=True)


for index in INDICES:

    rslt = list()
    for iter_ in range(NUM_DRAWS):

        options = options_base.copy()
        options["simulation_seed"] = iter_
        options["simulation_agents"] = NUM_SIMULATIONS

        simulate = rp.get_simulate_func(params_base, options)
        boot_df = simulate(params_base)

        crit_func = rp.get_crit_func(params_base, options, boot_df)
        p_wrapper_crit_func = partial(wrapper_crit_func, crit_func, params_base, index)

        point = params_base.loc[index, "value"]
        fd = approx_fprime([point], p_wrapper_crit_func, EPS)[0]

        rslt.append(fd)

    pkl.dump(rslt, open(f"score.{index[1]}.pkl", "wb"))
