"""Compute moments and weighting matrix for empirical datasets."""
import pandas as pd
from bld.project_paths import project_paths_join as ppj
from src.library.compute_moments import _replace_nans
from src.library.compute_moments import calc_restricted_choice_probabilities
from src.library.compute_moments import calc_restricted_wage_distribution
from src.library.compute_moments import calc_unrestricted_choice_probabilities
from src.library.compute_moments import calc_unrestricted_wage_distribution
from src.library.compute_moments import calc_very_restricted_choice_probabilities
from src.library.compute_moments import calc_very_restricted_wage_distribution
from src.library.compute_moments import get_weighting_matrix
from src.library.housekeeping import _save_to_pickle

if __name__ == "__main__":

    # load observed data
    df = pd.read_pickle(ppj("OUT_DATA", "df_hyp.pickle"))

    calc_moments = {
        "Choice Probabilities Very Restricted": calc_very_restricted_choice_probabilities,
        "Choice Probabilities Restricted": calc_restricted_choice_probabilities,
        "Choice Probabilities Unrestricted": calc_unrestricted_choice_probabilities,
        "Wage Distribution Very Restricted": calc_very_restricted_wage_distribution,
        "Wage Distribution Restricted": calc_restricted_wage_distribution,
        "Wage Distribution Unrestricted": calc_unrestricted_wage_distribution,
    }

    # compute empirical moments
    empirical_moments = {
        "Choice Probabilities Restricted": _replace_nans(calc_restricted_choice_probabilities(df)),
        "Choice Probabilities Unrestricted": _replace_nans(
            calc_unrestricted_choice_probabilities(df)
        ),
        "Choice Probabilities Very Restricted": _replace_nans(
            calc_very_restricted_choice_probabilities(df)
        ),
        "Wage Distribution Restricted": _replace_nans(calc_restricted_wage_distribution(df)),
        "Wage Distribution Unrestricted": _replace_nans(calc_unrestricted_wage_distribution(df)),
        "Wage Distribution Very Restricted": _replace_nans(
            calc_very_restricted_wage_distribution(df)
        ),
    }

    # compute weighting matrix
    weighting_matrix = get_weighting_matrix(
        data=df,
        empirical_moments=empirical_moments,
        calc_moments=calc_moments,
        n_bootstrap_samples=250,
        n_observations_per_sample=5000,
    )

    for res, name in zip([weighting_matrix, empirical_moments], ["weighting_matrix", "moments"]):

        _save_to_pickle(
            res,
            ppj("OUT_ANALYSIS", "msm_estimation", f"{name}_hyp.pickle"),
        )
