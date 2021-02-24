import pandas as pd
import numpy as np

vehicle_data_columns = ['t', 'vx', 'vy', 'Vx', 'Vy', 'Vr', 'vehicleslip_deg', 'vehicleslip_rad', 'oz_deg', 'oz_rad', 'delta_deg',
                        'delta_rad', 'turn_rX', 'turn_rY', 'turn_rR', 'au', 'av', 'ax', 'ay', 'ar', 'Ax', 'Ay', 'Ar',
                        'alphaz', 'alphaz_deg', 'beta_deg', 'beta_rad', 'lf_fx', 'lf_fy', 'rf_fx', 'rf_fy',
                        'rr_fx', 'rr_fy', 'lr_fx', 'lr_fy', 'lf_alpha', 'rf_alpha', 'rr_alpha', 'lr_alpha',
                        'lf_lock', 'rf_lock', 'rr_lock', 'lr_lock', 'lf_fz', 'rf_fz', 'rr_fz', 'lr_fz',
                        'theta_rad', 'theta_deg', 'Fx', 'Fy', 'Mz']


df = pd.DataFrame(np.zeros(shape=(1,len(vehicle_data_columns))), columns=vehicle_data_columns)

print(df)
