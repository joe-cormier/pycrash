
from data.defaults.config import default_dict
import numpy as np
import os

vehicle_mu = default_dict['vehicle_mu']

"""
calculates intervehicular forces using a sideswipe model (mutual crush + frictional forces)
validated using Funk () see validation directory for simulations and reports
"""

def ss(vehicle_list, crush_data, kmutual, i):
    """
    normal force is applied normal to the struck vehicle (vehicle 2)
    frictional force is applied along the impacting plane opposite to striking vehicle (vehicle 1) velocity
    """
    print(f'Sideswipe Model Accessed at t = {vehicle_list[0].veh_model.t[i]} seconds')
    # get velocity of impact point on V1 and V2 to relative velocity along impact edge
    # translate to global frame for comparison
    # if relative velocity is zero, friction force is zero

    # instead of relative velocity, try edge location - compare current to prior
    relative_edge_motion = crush_data.edge_loc[i] - crush_data.edge_loc[i-1]

    # crush force is a function of normal displacement and mutualstiffness
    # normal crush is always negative
    # TODO: need to test each condition

    fmutual = crush_data.normal_crush[i] * k_mutual

    # forces in vehicle 2 reference frame
    if vehicle_list[1].edgeimpact == 1:
        vehicle_list[1].veh_model.Fx[i] = fmutual
        vehicle_list[1].veh_model.Fy[i] = - 1 * np.sign(relative_edge_motion) * fmutual * vehicle_mu
        vehicle_list[1].veh_model.Mz[i] = -1 * vehicle_list[1].veh_model.Fx[i] * crush_data.impactp_veh2y[i] + vehicle_list[1].veh_model.Fy[i] * vehicle_list[1].edgeimpact_x1
    elif vehicle_list[1].edgeimpact == 2:
        vehicle_list[1].veh_model.Fx[i] = np.sign(relative_edge_motion) * fmutual * vehicle_mu
        vehicle_list[1].veh_model.Fy[i] = fmutual
        vehicle_list[1].veh_model.Mz[i] = -1 * vehicle_list[1].veh_model.Fx[i] * vehicle_list[1].edgeimpact_y1 + vehicle_list[1].veh_model.Fy[i] * crush_data.impactp_veh2x[i]
    elif vehicle_list[1].edgeimpact == 3:
        vehicle_list[1].veh_model.Fx[i] = -1 * fmutual
        vehicle_list[1].veh_model.Fy[i] = np.sign(relative_edge_motion) * fmutual * vehicle_mu
        vehicle_list[1].veh_model.Mz[i] = -1 * vehicle_list[1].veh_model.Fx[i] * crush_data.impactp_veh2y[i] - vehicle_list[1].veh_model.Fy[i] * vehicle_list[1].edgeimpact_x1
    elif vehicle_list[1].edgeimpact == 4:
        vehicle_list[1].veh_model.Fx[i] = -1 * np.sign(relative_edge_motion) * fmutual * vehicle_mu
        vehicle_list[1].veh_model.Fy[i] = -1 * fmutual
        vehicle_list[1].veh_model.Mz[i] = vehicle_list[1].veh_model.Fx[i] * vehicle_list[1].edgeimpact_y1 + vehicle_list[1].veh_model.Fy[i] * crush_data.impactp_veh2x[i]


vehicle_list[1].veh_model.Mz[i]    # forces in Vehicle 2 reference frame:
    fnorm = kmutual * impact_detect['normal_crush']  # normal forces
    ffriction = vehicle_mu * fnorm

    vehicle_list[0].veh_model.Fx = 0
    vehicle_list[0].veh_model.Fy = 0
    vehicle_list[0].veh_model.Mz = 0

    vehicle_list[1].veh_model.Fx = 0
    vehicle_list[1].veh_model.Fy = 0
    vehicle_list[1].veh_model.Mz = 0

    # calculate force and moment applied to each vehicle
    # striking vehicle
    # translate forces to veh1 frame, add Fx1, Fy1, Fx2, Fy2 to vehicle instance



    # struck vehicle

    return vehicle_list
