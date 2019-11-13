import warnings

import pandas as pd
import numpy as np
import respy as rp

from estimagic.optimization.optimize import maximize
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

def get_bootstrap_sample(df, seed=None):
    
    np.random.seed(seed)
    
    # Create the bootstrap sample
    identifiers = df["Identifier"].unique()
    boot_ids = np.random.choice(identifiers, size=len(identifiers))

    agents = list()
    for i, id_ in enumerate(boot_ids):
        agent = df[df["Identifier"] == id_]
        agent.loc[slice(None), "Identifier"] = i
        agents.append(agent)
    boot_df = pd.concat(agents)
    
    return boot_df


def run_bootstrap(df, params, options, constr, num_boots, is_perturb=False):

    boot_params = pd.DataFrame(index=params.index)
    identifiers = df["Identifier"].unique()

    for iter_ in range(num_boots):

        np.random.seed(iter_)
        
        boot_df = get_bootstrap_sample(df, seed=iter_)

        # Set up starting values
        params_start = params.copy()

        if is_perturb:           
            for index in params.index:
                lower, upper = params_start.loc[index, ["lower", "upper"]]
                params_start.loc[index, "value"] = np.random.uniform(lower, upper)

            for dict_ in constr:
                try:
                    stat = params.loc[(dict_["loc"]), "value"].values
                except:
                    stat = params.loc[(dict_["loc"]), "value"]
                params_start.loc[(dict_["loc"]), "value"] = stat

        crit_func = rp.get_crit_func(params, options, boot_df)

        results, params_rslt = maximize(
                    crit_func, params_start, 
                    "nlopt_bobyqa", 
                    algo_options={"maxeval": 100}, 
                    constraints=constr, 
        )

        boot_params[f"bootstrap_{iter_}"] = params_rslt["value"]
        
    return boot_params
