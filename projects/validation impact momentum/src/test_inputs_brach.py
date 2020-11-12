import pandas as pd
test_matrix = pd.read_excel('/home/jmc/Documents/pycrash/projects/validation impact momentum/docs/Brach Matrix.xlsx',
                            sheet_name='input')
test_data = {}
for index, row in test_matrix.iterrows():
    test_data[row.ID] = {'type':row.Type,
                         'vehicle': row.Vehicle,
                         'barrier': 'barrier',
                         'impact_speed': row.Vimpact,  # [mph]
                         'd_impact': row.d1,  # <- radius to impact center [ft]
                         'phi_impact': -1 * row.phi,  # <- angle to impact center (ccw [+])
                         'gamma': -1 * row.gamma,  # crush surface angle
                         'cor_test': row.COR,
                         'impulse_ratio': row.mu,
                         'dvx_test': -1 * row.dvx,  # [mph]
                         'dvy_test': row.dvy,  # [mph]
                         'domega_test': -1 * row.omega}  # [deg/s]

input_dir = '/home/jmc/Documents/pycrash/projects/validation impact momentum/data/input'
with open(os.path.join(input_dir, 'brachTestData.pkl'), 'wb') as handle:
    pickle.dump(test_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

"""
test_data = {'CF11002': {'vehicle': 'FordFusion',
                         'barrier': 'barrier',
                         'impact_speed': 39.95,  # [mph]
                         'd_impact': 4.14,  # <- radius to impact center [ft]
                         'phi_impact': -29,  # <- angle to impact center (ccw [+])
                         'gamma': -74.6,  # crush surface angle
                         'cor_test': 0,
                         'impulse_ratio': 85.18,
                         'dvx_test': -38.49 * 0.681818,  # [mph]
                         'dvy_test': 10.69 * 0.681818,  # [mph]
                         'domega_test': -102.75},  # [deg/s]

             'CF10017': {'vehicle': 'FordFusion',
                         'barrier': 'barrier',
                         'impact_speed': 40,  # [mph]
                         'd_impact': 4.6,  # <- radius to impact center [ft]
                         'phi_impact': -23.8,  # <- angle to impact center (ccw [+])
                         'gamma': -74.6,  # crush surface angle
                         'cor_test': 0,
                         'impulse_ratio': 85.18,
                         'dvx_test': -54.82 * 0.681818,
                         'dvy_test': 9.94 * 0.681818,
                         'domega_test': -157.23},

             'CF10023': {'vehicle': 'FordFusion',
                         'barrier': 'barrier',
                         'impact_speed': 40,  # [mph]
                         'd_impact': 4.6,  # <- radius to impact center [ft]
                         'phi_impact': -26.3,  # <- angle to impact center (ccw [+])
                         'gamma': -77,  # crush surface angle
                         'cor_test': 0,
                         'impulse_ratio': 97.5,
                         'dvx_test': -31.9 * 0.681818,
                         'dvy_test': 7.3 * 0.681818,
                         'domega_test': -196.28},

             'CF10013':  {'vehicle': 'FordFusion',
                          'barrier': 'barrier',
                          'impact_speed': 40.01589842,
                          'd_impact': 4.6,
                          'phi_impact': 26.3,
                          'gamma': 77,
                          'cor_test': 0,
                          'impulse_ratio': 97.5,
                          'dvx_test': 31.86135514,
                          'dvy_test': 7.2613617,
                          'domega_test': 196.28}
             }
"""
