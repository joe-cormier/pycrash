"""
functions for detecting impact using point (Veh1) and edge (Veh2)
"""
import pandas as pd
import numpy as np
import math

def detect(i, impactNum, vehicle_list, impPointEdge, strikingVehicle, struckVehicle, crush_data):
    """
    detects impacts in sequence using impact loaction and contant plane lists
    """
    #print(f'Vehicle 1 time = {vehicle_list[0].model.t[i]}')
    # current location of impact point - vehicle 1
    cgx1 = vehicle_list[strikingVehicle].model.Dx[i]  # take last value in Dx
    cgy1 = vehicle_list[strikingVehicle].model.Dy[i]  # take last value in Dy
    theta_rad1 = vehicle_list[strikingVehicle].model.theta_rad[i]

    impactp_gx = cgx1 + impPointEdge[impactNum]['impact_points'][0] * math.cos(theta_rad1) - impPointEdge[impactNum]['impact_points'][1] * math.sin(theta_rad1)
    impactp_gy = cgy1 + impPointEdge[impactNum]['impact_points'][0] * math.sin(theta_rad1) + impPointEdge[impactNum]['impact_points'][1] * math.cos(theta_rad1)

    # impact edge - vehicle 2
    cgx2 = vehicle_list[struckVehicle].model.Dx[i]
    cgy2 = vehicle_list[struckVehicle].model.Dy[i]
    theta_rad2 = vehicle_list[struckVehicle].model.theta_rad[i]

    # impact point in veh2 reference frame
    impactp_veh2x = ((impactp_gx-cgx2) * math.cos(theta_rad2) + (impactp_gy-cgy2) * math.sin(theta_rad2))
    impactp_veh2y = (-1 * (impactp_gx-cgx2) * math.sin(theta_rad2) + (impactp_gy-cgy2) * math.cos(theta_rad2))

    """
    calculate relative position of impact point and impact edge
    save data to refer to determine relative velocity
    edge_loc is the location of the impact point along the impact edge,
    moving clockwise
    """
    # edgeimpact_points = (x1, y1, x2, y2)

    crush_data.impact[i] = False
    if vehicle_list[struckVehicle].edgeimpact == 0:
        crush_data.normal_crush[i] = impactp_veh2x - impPointEdge[impactNum]['edgeimpact_points'][0]
        crush_data.edge_loc[i] = impPointEdge[impactNum]['edgeimpact_points'][1] - impactp_veh2y
        if (crush_data.normal_crush[i] <= 0) & (impactp_veh2y >= impPointEdge[impactNum]['edgeimpact_points'][1]) & (impactp_veh2y <= impPointEdge[impactNum]['edgeimpact_points'][3]):
            crush_data.impact[i] = True
    elif vehicle_list[struckVehicle].edgeimpact == 1:
        crush_data.normal_crush[i] = impactp_veh2y - impPointEdge[impactNum]['edgeimpact_points'][1]
        crush_data.edge_loc[i] = impPointEdge[impactNum]['edgeimpact_points'][0] - impactp_veh2x
        if (crush_data.normal_crush[i] <= 0) & (impactp_veh2x <= impPointEdge[impactNum]['edgeimpact_points'][0]) & (impactp_veh2x >= impPointEdge[impactNum]['edgeimpact_points'][2]):
            crush_data.impact[i] = True
    elif vehicle_list[struckVehicle].edgeimpact == 2:
        crush_data.normal_crush[i] = impPointEdge[impactNum]['edgeimpact_points'][0] - impactp_veh2x
        crush_data.edge_loc[i] = impPointEdge[impactNum]['edgeimpact_points'][1] - impactp_veh2y
        if (crush_data.normal_crush[i] <= 0) & (impactp_veh2y <= impPointEdge[impactNum]['edgeimpact_points'][1]) & (impactp_veh2y >= impPointEdge[impactNum]['edgeimpact_points'][3]):
            crush_data.impact[i] = True
    elif vehicle_list[struckVehicle].edgeimpact == 3:
        crush_data.normal_crush[i] = impPointEdge[impactNum]['edgeimpact_points'][1] - impactp_veh2y
        crush_data.edge_loc[i] = impactp_veh2x - impPointEdge[impactNum]['edgeimpact_points'][0]
        if (crush_data.normal_crush[i] < 0) & (impactp_veh2x >= impPointEdge[impactNum]['edgeimpact_points'][0]) & (impactp_veh2x <= impPointEdge[impactNum]['edgeimpact_points'][2]):
            crush_data.impact[i] = True

    crush_data.ImpactNumber[i] = impactNum
    crush_data.impactp_veh2x[i] = impactp_veh2x
    crush_data.impactp_veh2y[i] = impactp_veh2y

    return crush_data
