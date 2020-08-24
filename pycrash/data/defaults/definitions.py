"""
repository for all variables used in pycrash modulues
"""
variable_definitions = {
'delta_deg':'tire steer angle (degrees)',
'delta_rad':'tire steer angle (radians)',
'beta_deg':'vehicle slip angle (degrees)',
'beta_rad':'vehicle slip angle (radians)',
'theta_deg':'vehicle heading angle (degrees)',
'theta_rad':'vehicle heading angle (radians)',
'vehicleslip_deg':'vehicle slip angle (degrees)',
'vehicleslip_rad':'vehicle slip angle (radians)',
'lf_alpha':'left front tire slip angle in tire reference frame (radians)',
'rf_alpha':'right front tire slip angle in tire reference frame (radians)',
'rr_alpha':'right rear tire slip angle in tire reference frame (radians)',
'lr_alpha':'left rear tire slip angle in tire reference frame (radians)'
}

def define(variable):
    print(f"{variable} is defined as: )
    return variable_definitions['variable']
