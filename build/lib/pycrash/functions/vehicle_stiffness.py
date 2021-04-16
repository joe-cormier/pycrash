
import math
import numpy as np
# frontal barrier test:
# generating constant stiffness crash plot


def crash_plot(test_data, veh):
    """
    Derive vehicle stiffness values (A, B) from crash test data
    see Stuble for detailed explanation
    Struble, D. (2014). Automotive Accident Reconstruction Practices and Principles. Boca Raton (FL), CRC Press.
    """
    c_list = test_data['test_crush']
    if max(c_list) == 0:  # create orinate for zero crush
        beta = 1
        CE = 0.5 * (veh.weight / 32.2) * (test_data['test_speed'] * 1.46667)**2 * (1 - test_data['epsilon']**2)  # [ft-lb]
        ECF = math.sqrt(2 * beta * CE * 12 / test_data['damage_length'])  # [Energy Crush Factor]
        return 0, ECF
    else:
        c_ave = 1 / 10 * (c_list[0] + 2 * c_list[1] + 2 * c_list[2] + 2 * c_list[3] + 2 * c_list[4] + c_list[5])
        # form factor
        beta = 1 / (15 * c_ave**2) * (c_list[0]**2 + c_list[0] * c_list[1] + 2 * c_list[1]**2 +
                                             c_list[1] * c_list[2] + 2 * c_list[2]**2 + c_list[2] * c_list[3] +
                                             2 * c_list[3]**2 + c_list[3] * c_list[4] + 2 * c_list[4]**2 +
                                             c_list[4] * c_list[5] + c_list[5]**2)

        CE = 0.5 * (veh.weight / 32.2) * (test_data['test_speed'] * 1.46667)**2 * (1 - test_data['epsilon']**2)  # [ft-lb]



        # crash plot points
        x = beta * c_ave
        ECF = math.sqrt(2 * beta * CE * 12 / test_data['damage_length'])  # [Energy Crush Factor - converting CE to in-lb]

        print(f'average crush = {c_ave}, form factor = {beta}, crush energy = {CE}')
        return x, ECF
