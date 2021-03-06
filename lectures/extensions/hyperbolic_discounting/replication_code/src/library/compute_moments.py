"""Functions shared across modules."""
import numpy as np
import respy as rp
from respy.method_of_simulated_moments import _harmonize_input


def calc_choice_probabilities(df):
    """Compute choice probabilities by period."""
    return df.groupby("Period").Choice.value_counts(normalize=True).unstack()


def calc_very_restricted_choice_probabilities(df):
    """Compute choice probabilities for agents under two choice restrictions."""
    return (
        df.query("Policy == 'veryrestricted'")
        .groupby("Period")
        .Choice.value_counts(normalize=True)
        .unstack()
    )


def calc_restricted_choice_probabilities(df):
    """Compute choice probabilities for agents under one choice restriction."""
    return (
        df.query("Policy == 'restricted'")
        .groupby("Period")
        .Choice.value_counts(normalize=True)
        .unstack()
    )


def calc_unrestricted_choice_probabilities(df):
    """Compute choice probabilities for unrestricted agents."""
    return (
        df.query("Policy == 'unrestricted'")
        .groupby("Period")
        .Choice.value_counts(normalize=True)
        .unstack()
    )


def calc_wage_distribution(df):
    """Compute mean and standard deviation of wages, by period."""
    return df.groupby(["Period"])["Wage"].describe()[["mean", "std"]]


def calc_very_restricted_wage_distribution(df):
    """Compute per-period mean and std of wages for agents under two choice restrictions."""
    return (
        df.query("Policy == 'veryrestricted' and Choice == 'a' or Choice == 'b'")
        .groupby(["Period"])["Wage"]
        .describe()[["mean", "std"]]
    )


def calc_restricted_wage_distribution(df):
    """Compute per-period mean and std of wages for agents under one choice restriction."""
    return (
        df.query("Policy == 'restricted' and Choice == 'a' or Choice == 'b'")
        .groupby(["Period"])["Wage"]
        .describe()[["mean", "std"]]
    )


def calc_unrestricted_wage_distribution(df):
    """Compute mean and standard deviation of wages, by period."""
    return (
        df.query("Policy == 'unrestricted' and Choice == 'a' or Choice == 'b'")
        .groupby(["Period"])["Wage"]
        .describe()[["mean", "std"]]
    )


def _replace_nans(df):
    """Replace missing values in data."""
    return df.fillna(0)


def get_weighting_matrix(
    data,
    empirical_moments,
    calc_moments,
    n_bootstrap_samples,
    n_observations_per_sample,
    replace_missing_weights=None,
):
    """Compute a diagonal weighting matrix for estimation with MSM.

    Weights are the inverse bootstrap variances of the observed sample moments.

    Args:
        data (pandas.DataFrame): Dataframe containing individual observations.
            Must contain index named "Identifier" by which observations are sampled.
        empirical_moments (dict): Dictionary containing empirical moments in the
            form of pandas.DataFrame or pandas.Series.
        calc_moments (dict): Dictionary containing moment functions.
        n_bootstrap_samples (int): Number of samples that should be boostrapped.
        n_observations_per_sample (int): Observations per bootstrap sample.
        replace_missing_weights (None or float): Can be used to replace missing
            weights with a float value. If none, in cases where where weights are
            computed to be missing/infinite (i.e. if variances are 0), weights
            are set to zero.

    Returns:
        numpy.array: Diagonal weighting matrix with dimensions
            RxR where R denotes the number of moments.
    """
    data = data.copy()
    np.random.seed(123)
    flat_empirical_moments = rp.get_flat_moments(empirical_moments)
    index_base = data.index.get_level_values("Identifier").unique()
    calc_moments = _harmonize_input(calc_moments)
    # Create bootstrapped moments.
    moments_sample = []
    for _ in range(n_bootstrap_samples):
        ids_boot = np.random.choice(index_base, n_observations_per_sample, replace=False)
        moments_boot = {k: func(data.loc[ids_boot]) for k, func in calc_moments.items()}
        flat_moments_boot = rp.get_flat_moments(moments_boot)
        flat_moments_boot = flat_moments_boot.reindex_like(flat_empirical_moments)
        flat_moments_boot = flat_moments_boot.fillna(0)
        moments_sample.append(flat_moments_boot)

    # Compute variance for each moment and construct diagonal weighting matrix.
    moments_var = np.array(moments_sample).var(axis=0)

    # The variance of missing moments is nan. Unless a replacement variance is
    # specified, their inverse variance will be set to 0.
    diagonal = moments_var ** (-1)
    if replace_missing_weights is None:
        diagonal = np.nan_to_num(diagonal, nan=0, posinf=0, neginf=0)
    else:
        diagonal = np.nan_to_num(
            moments_var,
            nan=replace_missing_weights,
            posinf=replace_missing_weights,
            neginf=replace_missing_weights,
        )

    weighting_matrix = np.diag(diagonal)

    # Checks weighting matrix.
    if np.isnan(weighting_matrix).any() or np.isinf(weighting_matrix).any():
        raise ValueError("Weighting matrix contains NaNs or infinite values.")

    return weighting_matrix
