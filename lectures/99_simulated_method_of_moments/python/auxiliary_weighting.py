""" Auxiliary file containing code for the weighting matrix for the notebook on simulated method of moments estimation.
"""

import numpy as np
import pandas as pd




def moments_dict_to_list(moments_dict):
    """This function constructs a list of available moments based on the moment dictionary."""
    moments_list = []
    for group in moments_dict.keys():
        for period in moments_dict[group].keys():
            moments_list.extend(moments_dict[group][period])
    return moments_list
