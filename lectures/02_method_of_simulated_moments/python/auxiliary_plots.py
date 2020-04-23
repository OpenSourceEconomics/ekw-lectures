""" Auxiliary file containing functions for plots for the notebook on simulated method of moments estimation.
"""
import copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import respy as rp


def plot_criterion_params(params, param_names, criterion_msm, radius): 
    """Plot criterion_msm for all values in params given radius (percentage deviation from value in 
       params dataframe). 
    """
    
    true_values = [params.loc[name, "value"] for name in param_names]
    deviations = [abs(val)*radius for val in true_values]
    lbounds = [params.loc[name, "value"] - dev for name, dev in zip(param_names, deviations)]
    ubounds = [params.loc[name, "value"] + dev for name, dev in zip(param_names, deviations)]
    detail = 20         
    
    for idx in range(len(param_names)):        
        parameters = params.copy()
        # Define grid of parameter values and calculate the criterion function value for this grid.
        x_grid = np.linspace(lbounds[idx], ubounds[idx], detail)
        fvals_grid = ([])
        for param in x_grid:
            parameters.loc[param_names[idx],'value'] = param
            fval = criterion_msm(parameters)
            fvals_grid.append(fval)
       
        # Plot criterion function for the calculated values. 
        plt.xticks(np.linspace(lbounds[idx], ubounds[idx],num=5))
        plt.plot(x_grid, fvals_grid)
        plt.axvline(true_values[idx], color="#A9A9A9", linestyle="--", label="True Value")
        plt.xlabel(param_names[idx])
        
        plt.show()
    
    
def plot_moments_choices(moments_obs, moments_sim):
    
    moments = [moments_obs, moments_sim]
    titles = ["Data Moments", "Simulated Moments"]
    
    for idx in [0,1]:
        df = pd.DataFrame(moments[idx]['Choice Frequencies']).transpose()
        df = df.rename(columns={0: "fishing", 1: "hammock"})

        plt.subplot(1, 2, idx+1)
        plt.ylim((0,1))
        plt.title(titles[idx])
        plt.plot(pd.DataFrame(moments[idx]['Choice Frequencies']).transpose())
        plt.xlabel("Period")
        plt.ylabel("Choice Frequencies")
        if idx == 1:
            plt.legend(df.columns, loc="best")
    
    plt.tight_layout()
    plt.show()
    
    
def plot_moments_wage(moments_obs, moments_sim):
    
    df_sim = pd.DataFrame(moments_sim['Wage Distribution']).transpose()    
    df_obs = pd.DataFrame(moments_obs['Wage Distribution']).transpose()    
    
    plt.subplot(1, 2, 1)
    plt.title('Mean')
    plt.plot(df_obs[0])
    plt.plot(df_sim[0])
    plt.xlabel('Period')
    
    plt.subplot(1, 2, 2)
    plt.title('Std')
    plt.plot(df_obs[1], label = "observed")
    plt.plot(df_sim[1], label = "simulated")
    plt.legend(loc="best")
    plt.xlabel('Period')
    
    plt.tight_layout()
    plt.show()
    
    
def plot_chatter(seeds, criterion_smm, kwargs):
    
    args = copy.deepcopy(kwargs)
    criterion_values =[]
    
    for seed in seeds:
        args['options']['simulation_seed'] = seed
        val = criterion_smm(args['params'], 
                            args['options'], 
                            args['weighting_matrix'],
                            args['moments_obs'],
                            args['choice_options'])

        criterion_values.append(val)

    plt.plot(seeds, criterion_values, color='C1')
    plt.ylim(-1,40)
    plt.title('Criterion function for different simulation seeds')
    plt.ylabel('Criterion function')
    plt.xlabel('Seed') 
    

def plot_chatter_numagents_sim(seeds, num_agents, criterion_smm, kwargs):
    
    args = copy.deepcopy(kwargs)
    results = pd.DataFrame(columns=num_agents)

    for num in num_agents:
        args['options']['simulation_agents'] = num
        criterion_values =[]
        for seed in seeds:
            args['options']['simulation_seed'] = seed

            val = criterion_smm(args['params'], 
                                args['options'], 
                                args['weighting_matrix'],
                                args['moments_obs'],
                                args['choice_options'])

            criterion_values.append(val)

        results[num] = criterion_values

        plt.plot(seeds, results[num], label=num)
        plt.ylim(-1,40)
        plt.title('Increasing only the number of simulated agents')
        plt.ylabel('Criterion function')
        plt.xlabel('Seed')
        plt.legend(loc='best')
        
        
def plot_chatter_numagents_both(seeds, num_agents, get_moments, criterion_smm, kwargs):
    
    args = copy.deepcopy(kwargs)
    # Initialize df to hold results.
    results = pd.DataFrame(columns=num_agents)

    # Increase number of agents in real data.
    for num in num_agents:
        options_true = args['options'].copy()
        options_true["simulation_agents"] = num
        simulate = rp.get_simulate_func(args['params'], options_true)
        data_true = simulate(args['params'])
        moments_true = get_moments(data_true, args['choice_options'])

    # Increase number of agents in simulated model.        
        options_chatter = args['options'].copy()
        options_chatter["simulation_agents"] = num 
        criterion_values =[]
        for seed in seeds:
            options_chatter["simulation_seed"] = seed
            val = criterion_smm(args['params'], 
                                options_chatter, 
                                args['weighting_matrix'], 
                                moments_true, 
                                args['choice_options'])

            criterion_values.append(val)

        results[num] = criterion_values

    # Plot the results.
        plt.plot(seeds, results[num], label=num)
        plt.ylim(-1,40)
        plt.title('Increasing the number of Observed and Simulated agents')
        plt.ylabel('Criterion function')
        plt.xlabel('Seed')
        plt.legend(loc='best')