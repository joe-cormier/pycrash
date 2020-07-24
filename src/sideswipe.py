
import os
from data.defaults.config import default_dict


vehicle_mu = default_dict['vehicle_mu']

"""
calculates intervehicular forces using a sideswipe model (mutual crush + frictional forces)
validated using Funk () see validation directory for simulations and reports
"""


def ss(vehicle_list, impact_detect):
    """
    normal force is applied normal to the struck vehicle (vehicle 2)
    frictional force is applied along the impacting plane opposite to striking vehicle (vehicle 1) velocity
    """
    print(f'Sideswipe Model Accessed at t = {vehicle_list[0].veh_model.t.iloc[-1]} seconds')
    # get relative velocity along impacting plane




    # calculate force and moment applied to each vehicle
    # striking vehicle
    # translate forces to veh1 frame, add Fx1, Fy1, Fx2, Fy2 to vehicle instance



    # struck vehicle
