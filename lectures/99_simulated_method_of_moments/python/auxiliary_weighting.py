""" Auxiliary file containing code for the weighting matrix for the notebook on simulated method of moments estimation.
"""

import numpy as np
import pandas as pd
from python.auxiliary_core import *




def moments_dict_to_list(moments_dict):
    """This function constructs a list of available moments based on the moment dictionary."""
    moments_list = []
    for group in moments_dict.keys():
        for period in moments_dict[group].keys():
            moments_list.extend(moments_dict[group][period])
    return moments_list


def get_weighing_matrix(df_base, choice_options, num_boots, num_agents_smm):
    """This function constructs the weighing matrix."""
    # Ensure reproducibility
    np.random.seed(123)

    # Distribute clear baseline information.
    #index_base = df_base.index.get_level_values('Identifier').unique()
    index_base = df_base['Identifier'].unique()
    moments_base = get_moments(df_base, choice_options)
    num_boots_max = num_boots * 2

    # Initialize counters to keep track of attempts.
    num_valid, num_attempts, moments_sample = 0, 0, []

    while True:

        try:
            sample_ids = np.random.choice(index_base, num_agents_smm, replace=False)
            moments_boot = get_moments(df_base.loc[sample_ids, :], choice_options)

            # We want to confirm that we have valid values for all required moments that we were
            # able to calculate on the observed dataset.
            for group in ['Choice Probabilities', 'Wage Distribution']:
                for period in moments_base[group].keys():
                    if period not in moments_boot[group].keys():
                        raise NotImplementedError

            moments_sample.append(moments_boot)

            num_valid += 1
            if num_valid == num_boots:
                break

            # We need to terminate attempts that just seem to not work.
            if num_attempts > num_boots_max:
                raise NotImplementedError("... too many samples needed for matrix")

        except NotImplementedError:
            continue

        num_attempts += 1

    # Construct the weighing matrix based on the sampled moments.
    stats = []
    for moments_boot in moments_sample:
        stats.append(moments_dict_to_list(moments_boot))

    moments_var = np.array(stats).T.var(axis=1)

    # We need to deal with the case that the variance for some moments is zero. This can happen
    # for example for the choice probabilities if early in the lifecycle nobody is working. This
    # will happen with the current setup of the final schooling moments, where we simply create a
    # grid of potential final schooling levels and fill it with zeros if not observed in the
    # data. We just replace it with the weight of an average moment.
    is_zero = moments_var <= 1e-10

    # TODO: As this only applies to the moments that are bounded between zero and one,
    #  this number comes up if I calculate the variance of random uniform variables.
    moments_var[is_zero] = 0.1

    if np.all(is_zero):
        raise NotImplementedError('... all variances are zero')
    if np.any(is_zero):
        print('... some variances are zero')

    return np.diag(moments_var ** (-1))