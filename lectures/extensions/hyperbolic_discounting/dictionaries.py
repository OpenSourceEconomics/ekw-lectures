"""Auxiliary dictionaries for `hyperbolic_discounting.ipynb`"""

policyDict = {"unrestricted": "Unr", "restricted": "R", "veryrestricted": "VR"}
colorDict = {"a": "#eb760a", "b": "#43aa8b", "edu": "#f9c74f", "home": "#577590"}
labelDict = {"a": "Occ. A", "b": "Occ. B", "edu": "Education", "home": "Home"}
titleDict = {
    "True": r"True ($\beta = 0.8, \delta = 0.95$)",
    "Exponential": r"Exponential ($\beta = 1, \delta = 0.938$)",
    "Global_min": r"Global minimum ($\beta = 0.83, \delta = 0.948$)",
}
styleDict = {
    "True": {"line": {"linestyle": "-"}, "fill": {"facecolor": "grey", "alpha": 0.35}},
    "Exponential": {
        "line": {"linestyle": "-", "marker": "D", "mfc": "white"},
        "fill": {"hatch": "//", "facecolor": "white", "edgecolor": "black", "alpha": 0.3},
    },
    "Global_min": {
        "line": {"linestyle": "-", "marker": "D", "mfc": "black"},
        "fill": {"hatch": "\\", "facecolor": "white", "edgecolor": "black", "alpha": 0.3},
    },
}
