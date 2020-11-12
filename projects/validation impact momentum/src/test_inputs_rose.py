"""
Rose 2006 SAE paper
Rose, N., et al. (2006). Restitution Modeling for Crush Analysis: Theory and Validation. Society of Automotive Engineers. No. 2006-01-0908.
"""

test_data = {}
test_data['4363'] = {'v1_cg_ic': 2.6,           # radial distance from cg to impact center
                     'v1_theta_cg_ic': 23.8,    # polar angle to impact center
                     'v1_head_angle': 180,      # heading angle
                     'v1_vx': 35.1,             # initial velocity (mph)
                     'v2_cg_ic': 5.7,           # radial distance from cg to impact center
                     'v2_theta_cg_ic': 10.6,    # polar angle to impact center
                     'v2_head_angle': 32,       # heading angle
                     'v2_vx': 35,               # initial velocity (mph)
                     'impact_norm_deg': 55,     # orientation of normal direction (deg)
                     'cor': 0.126,              # coefficient of restitution
                     'critical_ir': -0.51,      # critical impulse ratio
                     'impulse_ratio': 1,        # impulse ratio (%)
                     'v1_domega': 31,           # vehicle 1 change in omega (deg/s)
                     'v1_dv': 39.5,             # vehicle 1 delta-V (mph)
                     'v2_domega': 182,          # vehicle 2 change in omega (deg/s)
                     'v2_dv': 29.1,             # vehicle 2 delta-V (mph)
                     }

test_data['4364'] = {'v1_cg_ic': 2.3,
                     'v1_theta_cg_ic': 45.7,
                     'v1_head_angle': 180,
                     'v1_vx': 35,
                     'v2_cg_ic': 7.1,
                     'v2_theta_cg_ic': 11.2,
                     'v2_head_angle': 30,
                     'v2_vx': 34.9,
                     'impact_norm_deg': 51.9,
                     'cor': 0.089,
                     'critical_ir': -0.42,
                     'impulse_ratio': 1,
                     'v1_domega': 108,
                     'v1_dv': 40.1,
                     'v2_domega': 148,
                     'v2_dv': 26.6,
                     }

test_data['4438'] = {'v1_cg_ic': 2.8,
                     'v1_theta_cg_ic': 35.3,
                     'v1_head_angle': 180,
                     'v1_vx': 34.7,
                     'v2_cg_ic': 5,
                     'v2_theta_cg_ic': 13.2,
                     'v2_head_angle': 30,
                     'v2_vx': 35,
                     'impact_norm_deg': 50.7,
                     'cor': 0.095,
                     'critical_ir': -0.44,
                     'impulse_ratio': 1,
                     'v1_domega': 68,
                     'v1_dv': 39.7,
                     'v2_domega': 166,
                     'v2_dv': 27.8,
                     }

test_data['4474'] = {'v1_cg_ic': 2.9,
                     'v1_theta_cg_ic': 34.7,
                     'v1_head_angle': 180,
                     'v1_vx': 35,
                     'v2_cg_ic': 5.5,
                     'v2_theta_cg_ic': 15.2,
                     'v2_head_angle': 31.6,
                     'v2_vx': 35,
                     'impact_norm_deg': 51.8,
                     'cor': 0.150,
                     'critical_ir': -0.40,
                     'impulse_ratio': 1,
                     'v1_domega': 40,
                     'v1_dv': 40.5,
                     'v2_domega': 194,
                     'v2_dv': 28.7,
                     }