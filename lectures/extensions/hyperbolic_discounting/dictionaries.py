"""Auxiliary dictionaries for `hyperbolic_discounting.ipynb`."""

policy_dict = {"unrestricted": "Unr", "restricted": "R", "veryrestricted": "VR"}
color_dict = {"a": "#eb760a", "b": "#43aa8b", "edu": "#f9c74f", "home": "#577590"}
label_dict = {"a": "Occ. A", "b": "Occ. B", "edu": "Education", "home": "Home"}
title_dict = {
    "true": r"True ($\beta = 0.8, \delta = 0.95$)",
    "exponential": r"Exponential ($\beta = 1, \delta = 0.938$)",
    "global_min": r"Global minimum ($\beta = 0.83, \delta = 0.948$)",
}
style_dict = {
    "true": {"line": {"linestyle": "-"}, "fill": {"facecolor": "grey", "alpha": 0.35}},
    "exponential": {
        "line": {"linestyle": "-", "marker": "D", "mfc": "white"},
        "fill": {"hatch": "//", "facecolor": "white", "edgecolor": "black", "alpha": 0.3},
    },
    "global_min": {
        "line": {"linestyle": "-", "marker": "D", "mfc": "black"},
        "fill": {"hatch": "\\", "facecolor": "white", "edgecolor": "black", "alpha": 0.3},
    },
}
