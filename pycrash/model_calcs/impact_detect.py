"""
functions for detecting impact using point (Veh1) and edge (Veh2)
"""
import pandas as pd
import numpy as np
import math

def detect(vehicle_list, i, crush_data = None):
    #print('-- looking for impact --')
    #print(f'Vehicle 1 time = {vehicle_list[0].model.t[i]}')
    # TODO: assuming that vehicle_list = [veh1, veh2] - can fix by checking for impact point definition
    # current location of impact point - vehicle 1
    cgx1 = vehicle_list[0].model.Dx[i]  # take last value in Dx
    cgy1 = vehicle_list[0].model.Dy[i]  # take last value in Dy
    theta_rad1 = vehicle_list[0].model.theta_rad[i]

    impactp_gx = cgx1 + vehicle_list[0].pimpact_x * math.cos(theta_rad1) - vehicle_list[0].pimpact_y * math.sin(theta_rad1)
    impactp_gy = cgy1 + vehicle_list[0].pimpact_x * math.sin(theta_rad1) + vehicle_list[0].pimpact_y * math.cos(theta_rad1)

    # impact plane - vehicle 2
    cgx2 = vehicle_list[1].model.Dx[i]
    cgy2 = vehicle_list[1].model.Dy[i]
    theta_rad2 = vehicle_list[1].model.theta_rad[i]

    # impact point in veh2 reference frame
    impactp_veh2x = ((impactp_gx-cgx2) * math.cos(theta_rad2) + (impactp_gy-cgy2) * math.sin(theta_rad2))
    impactp_veh2y = (-1 * (impactp_gx-cgx2) * math.sin(theta_rad2) + (impactp_gy-cgy2) * math.cos(theta_rad2))

    """
    print(f'Vehicle 2 Heading Angle = {theta_rad2 * 180 / math.pi} degrees')
    print(f'Impact Point in Veh2 Frame x = {impactp_veh2x}, y = {impactp_veh2y}')
    print(f'Impact Point location: x = {impactp_gx}, y = {impactp_gy}')
    print(f'Veh1 CG location: x = {cgx1}, y = {cgy1}')
    print(f'Veh2 CG location: x = {cgx2}, y = {cgy2}')
    """

    """
    calculate relative position of impact point and impact edge
    save data to refer to determine relative velocity
    edge_loc is the location of the impact point along the impact edge,
    moving clockwise
    """
    if i == 0:
        crush_data = pd.DataFrame(np.nan, index=np.arange(len(vehicle_list[0].driver_input.t)),
                                columns = ['impact', 'edge_loc', 'normal_crush', 'impactp_veh2x', 'impactp_veh2y'])

    crush_data.impact[i] = False
    if vehicle_list[1].edgeimpact == 1:
        crush_data.normal_crush[i] = impactp_veh2x - vehicle_list[1].edgeimpact_x1
        crush_data.edge_loc[i] = vehicle_list[1].edgeimpact_y1 - impactp_veh2y
        if (crush_data.normal_crush[i] <= 0) & (impactp_veh2y >= vehicle_list[1].edgeimpact_y1) & (impactp_veh2y <= vehicle_list[1].edgeimpact_y2):
            crush_data.impact[i] = True
    elif vehicle_list[1].edgeimpact == 2:
        crush_data.normal_crush[i] = impactp_veh2y - vehicle_list[1].edgeimpact_y1
        crush_data.edge_loc[i] = vehicle_list[1].edgeimpact_x1 - impactp_veh2x
        if (crush_data.normal_crush[i] <= 0) & (impactp_veh2x <= vehicle_list[1].edgeimpact_x1) & (impactp_veh2x >= vehicle_list[1].edgeimpact_x2):
            crush_data.impact[i] = True
    elif vehicle_list[1].edgeimpact == 3:
        crush_data.normal_crush = vehicle_list[1].edgeimpact_x1 - impactp_veh2x
        crush_data.edge_loc[i] = vehicle_list[1].edgeimpact_y1 - impactp_veh2y
        if (crush_data.normal_crush <= 0) & (impactp_veh2y <= vehicle_list[1].edgeimpact_y1) & (impactp_veh2y >= vehicle_list[1].edgeimpact_y2):
            crush_data.impact[i] = True
    elif vehicle_list[1].edgeimpact == 4:
        crush_data.normal_crush[i] = vehicle_list[1].edgeimpact_y1 - impactp_veh2y
        crush_data.edge_loc[i] = vehicle_list[1].edgeimpact_x1 - impactp_veh2x
        if (crush_data.normal_crush[i] < 0) & (impactp_veh2x >= vehicle_list[1].edgeimpact_x1) & (impactp_veh2x <= vehicle_list[1].edgeimpact_x2):
            crush_data.impact[i] = True

    crush_data.impactp_veh2x[i] = impactp_veh2x
    crush_data.impactp_veh2y[i] = impactp_veh2y

    return crush_data
