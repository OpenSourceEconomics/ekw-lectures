""" Auxiliary file containing functions for the notebook und simulated method of moments estimation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import respy as rp
import seaborn as sns
import respy as rp
from collections import defaultdict


def get_moments(df, choice_options):
    """Function for calculating moments for a dataset.
    Args:
    df(pd.DataFrame): Dataframe containing observations on choices of agents. Dataset must contain the following columns:
        - 'Period': Column containing time period of observation.
        - 'Identifier': Column containing the identifier of the agent for each observation.
        - 'Choice': Column containing the choice an agent as made in period for each observation.
        - 'Wage': Column containing the wage each agent has earned each period (should be np.nan if 
                  agent did not work in a given period)
    choice_options(list): List of possible choices. Needs to be specified manually because we need the full set of choice 
                          options for the choice probabilities and there can be cases where some choices are not realized 
                          by any agent and will thus not appear in the data.
    
    Returns:
    moments_dict(dictionary): Dictionary containing subdictionaries with the moments:
        - 'Choice Probability': Dictionary containing the proportion of agents who have chosen a given 
                                option each period for each option.
        - 'Wage Distribution':  Dictionary containing the mean and the standard deviation of wages for each period.
    --------------------------------------------------------------------------------------------------------------------    
    """
    periods = df['Period'].unique()

    moments_dict = {}
    
    # 1. Choice Probability for each period and each choice option
    df_indexed = df.set_index(['Identifier', 'Period'], drop=True)
    df_grouped_period = df_indexed.groupby(['Period'])
    info_period = df_grouped_period['Choice'].value_counts(normalize=True).to_dict()
    # Dictionary will give a period choice probability of 0 if a choice is not observed at all in a period.
    info_period = defaultdict(lambda: 0.00, info_period)

    choices_dict = dict.fromkeys(periods)

    for key in choices_dict.keys():
        choice_proba = []
        for choice in choice_options:
            choice_proba.append(info_period[(key,choice)])   
    
        choices_dict[key] = choice_proba  
    
    moments_dict['Choice Probabilities'] = choices_dict
    
    # 2. Wage Distribution
    periods = sorted(df['Period'].unique())
    df_indexed = df.set_index(['Identifier', 'Period'], drop=True)
    df_grouped_period = df_indexed.groupby(['Period'])
    
    # Describe wages to extract wage mean and std.
    info_period = df_grouped_period['Wage'].describe() 
    # Initialize wage dictionary with period as keys and add mean and std for each period.
    wages_dict = dict.fromkeys(info_period.index.to_list())
    for key in info_period.index.to_list():                
            wages_dict[key] = (info_period.loc[key,'mean'],info_period.loc[key,'std'])
    
    # Add wage mean and std to moments dict.
    moments_dict['Wage Distribution'] = wages_dict
    
    return moments_dict



def evaluate(params_cand, options, weighting_matrix, moments_obs, choice_options):
    params = params_cand.copy()
    periods = range(options["n_periods"])
    num_moments = len(np.diag(weighting_matrix))

    # Calculate simulated moments for model with candidate parameters.
    simulate = rp.get_simulate_func(params, options)
    df_sim = simulate(params)
    moments_sim = get_moments(df_sim, choice_options)
    
    # Check whether candidate parameters are valid inputs.
    stats_obs, stats_sim = [], []
    for group in moments_sim.keys():
        for period in periods:
            stats_obs.extend(moments_obs[group][(period)])
            stats_sim.extend(moments_sim[group][(period)])

    is_valid = len(stats_obs) == len(stats_sim) == num_moments
    
    # Calculate weigthted dot product of difference between real moments and 
    # simulated moments.
    if is_valid:
        stats_diff = np.array(stats_obs) - np.array(stats_sim)
        fval = np.dot(stats_diff, weighting_matrix)
        fval = float(np.dot(fval, stats_diff))
    else:
        fval = 1000000
        
    return fval


def plot_criterion_fun(params, param_name, lbounds, ubounds, xticks_steps, detail, criterion_args):
    """ Plots criterion function for one or multiple ranges of values for a single parameter in the model.
    Args:
    params(pd.DataFrame): Dataframe containing the parameters in the model.
    param_name(string): Name of the parameter that should be varied to plot the criterion function.
    lbounds(list): Lower bound of the range of parameter values that should be calculated. Multiple values can be 
                   specified to plot the criterion function at different ranges of the parameter values.
    ubounds(list): Upper bound of the range of parameter values that should be calculated. Must be the same length as
                    lbounds.
    xticks_steps(list): List that specifies the step size for the ticks of the xaxis.
    criterion_args(list): List of arguments that need to be specified for the criterion function which is called for 
                          plotting (Args: options, weighting_matrix, moments_obs, choice_options)
    detail(int): Number of parameter values that the criterion function should be calculated for. Determines
                 the accuracy of the plotted function. 
    Returns:
    plots 
    --------------------------------------------------------------------------------------------------------------------
    """
    params = params.copy()
    plt.figure(figsize=(8, 12), dpi=70, facecolor='w', edgecolor='k')
    plt.subplots_adjust(wspace=0.4) 
    
    for idx in range(len(lbounds)):
        # Position of subplot
        plt.subplot(len(lbounds), 1, idx+1)
        # Define grid of parameter values and calculate the criterion function value for this grid.
        x_grid = np.linspace(lbounds[idx], ubounds[idx], detail)
        fvals_grid = ([])
        for param in x_grid:
            params.loc[param_name,'value'] = param
            fval = evaluate(params, *criterion_args)
            fvals_grid.append(fval)
       
        # Plot criterion function for the calculated values. 
        plt.xticks(np.arange(lbounds[idx], ubounds[idx], step=xticks_steps[idx]))
        plt.grid(which='major')
        plt.plot(x_grid, fvals_grid, ".")
        plt.plot(x_grid, fvals_grid, color="orange")
        plt.xlabel(param_name)
        plt.ylabel('Criterion Function')
