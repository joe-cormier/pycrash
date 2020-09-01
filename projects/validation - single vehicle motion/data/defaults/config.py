
# Simulation Defaults
# time step for vehicle motion (seconds)
# time step for impact simulation (seconds)
# maximum available friction
# maximum tire slip angle (rad) default is 10 degrees
# intervehicle friction for sideswipe / impc models
# ---------------------------------------------------------------------------------------------
{
    'sim_defaults': [
	{
		'dt_motion':0.1,            	
		'dt_impact':0.0001,         	
		'mu_max':0.76,              	
		'alpha_max':0.174533,       	
		'vehicle_mu':0.3,          	
	}
    ]
}

# Plot Defaults
# (width, height) for plots
# overall theme for plots
# ----------------------------------------------------------------------------------------------
{
    'plot_defaults': [
	{
		'figure_size':(16, 9),      
		'plotly_theme':'plotly_white'  
	}
    ]
}
