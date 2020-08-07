
# Calculation Defaults
# ----------------------------------------------------------------------------------------------
"""
configuration for default values and settings
settings effect the following modulues:
vehicle
sdof_calculations
kinematics
kinematicstwo
"""
default_dict = {'dt_motion':0.1,            # time step for vehicle motion (seconds)
                'dt_impact':0.0001,         # time step for impact simulation (seconds)
                'mu_max':0.9,               # maximum available friction
                'alpha_max':0.349066,    # maximum tire slip angle (rad) default is 20 degrees
                'vehicle_mu':0.3}           # intervehicle friction for sideswipe / impc models

# Plot Defaults
# ----------------------------------------------------------------------------------------------
plot_settings = {'figure_size':(16, 9),      # (width, height) for plots
                'plotly_theme':'plotly_white'}  # overall theme for plots
