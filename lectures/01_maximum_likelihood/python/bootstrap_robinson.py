import respy as rp

from calibration_maximum_likelihood import run_bootstrap

NUM_BOOTS = 1000

# Get the basic model setup
params_base, options_base, df = rp.get_example_model("robinson", with_data=True)

params_base["lower"] = [0.9, 0.00, -0.20, 1.00, 0.0050, 0.001, -0.2]
params_base["upper"] = [1.0, 0.10,  0.00, 1.10, 0.0150, 0.030, +0.2]

# We will use estimagic and fix all parameters at their true values.
constr_base = [
    {"loc": ("shocks_sdcorr", "sd_fishing"), "type": "fixed"}, 
    {"loc": ("shocks_sdcorr", "sd_hammock"), "type": "fixed"}, 
    {"loc": ("shocks_sdcorr", "corr_hammock_fishing"), "type": "fixed"}, 
    {"loc": "wage_fishing", "type": "fixed"},
    {"loc": "nonpec_fishing", "type": "fixed"},
    {"loc": "nonpec_hammock", "type": "fixed"}
]

for i, index in enumerate([("delta", "delta"), ("shocks_sdcorr", "sd_hammock")]):

    constr = constr_base.copy()

    # We fix the discount factor and free "sd_hammock"
    if i == 1:
        constr.pop(1)
        constr.append({'loc': "delta", "type": "fixed"})

    for is_perturb in [True, False]:
        boot_params = run_bootstrap(df, params_base, options_base, constr, NUM_BOOTS, is_perturb)

        fname = f"bootstrap.{index[1]}_perturb_{str(is_perturb).lower()}.pkl"
        boot_params.to_pickle(fname)
