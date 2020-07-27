"""
functions for detecting impact using point (Veh1) and edge (Veh2)
"""
import math

def detect(vehicle_list, i):
    print('-- looking for impact --')
    print(f'Vehicle 1 time = {vehicle_list[0].veh_model.t[i]}')
    # TODO: assuming that vehicle_list = [veh1, veh2] - can fix by checking for impact point definition
    # current location of impact point - vehicle 1
    cgx1 = vehicle_list[0].veh_model.Dx[i]  # take last value in Dx
    cgy1 = vehicle_list[0].veh_model.Dy[i]  # take last value in Dy
    theta_rad1 = vehicle_list[0].veh_model.theta_rad[i]

    impactp_gx = cgx1 + vehicle_list[0].pimpact_x * math.cos(theta_rad1) - vehicle_list[0].pimpact_y * math.sin(theta_rad1)
    impactp_gy = cgy1 + vehicle_list[0].pimpact_x * math.sin(theta_rad1) + vehicle_list[0].pimpact_y * math.cos(theta_rad1)

    # impact plane - vehicle 2
    cgx2 = vehicle_list[1].veh_model.Dx[i]
    cgy2 = vehicle_list[1].veh_model.Dy[i]
    theta_rad2 = vehicle_list[1].veh_model.theta_rad[i]

    # impact point in veh2 reference frame
    impactp_veh2x = ((impactp_gx-cgx2) * math.cos(theta_rad2) + (impactp_gy-cgy2) * math.sin(theta_rad2))
    impactp_veh2y = (-1 * (impactp_gx-cgx2) * math.sin(theta_rad2) + (impactp_gy-cgy2) * math.cos(theta_rad2))

    print(f'Vehicle 2 Heading Angle = {theta_rad2 * 180 / math.pi} degrees')
    print(f'Impact Point in Veh2 Frame x = {impactp_veh2x}, y = {impactp_veh2y}')
    print(f'Impact Point location: x = {impactp_gx}, y = {impactp_gy}')
    print(f'Veh1 CG location: x = {cgx1}, y = {cgy1}')
    print(f'Veh2 CG location: x = {cgx2}, y = {cgy2}')

    impact = False
    crushdx = 0
    crushdy = 0
    mutual_crush = 0

    """
    calculate relative position of impact point and impact edge
    save data to refer to determine relative velocity
    edge_loc is the location of the impact point along the impact edge,
    moving clockwise
    """
    if i == 0:
        crush_data = pd.DataFrame(np.nan, index=np.arange(len(veh.driver_input.t)),
                                columns = ['impact', 'edge_loc', 'normal_crush'])

    if vehicle_list[1].edgeimpact == 1:
        crushdx = impactp_veh2x - vehicle_list[1].edgeimpact_x1
        if (crushdx <= 0) & (impactp_veh2y >= vehicle_list[1].edgeimpact_y1) & (impactp_veh2y <= vehicle_list[1].edgeimpact_y2):
            impact[i] = True
            edge_lo[i]c = vehicle_list[1].edgeimpact_y1 - impactp_veh2y
            normal_crush[i] = crushdx # extent of crush used to calculate force (sideswipe)
    elif vehicle_list[1].edgeimpact == 2:
        crushdy = impactp_veh2y - vehicle_list[1].edgeimpact_y1
        if (crushdy <= 0) & (impactp_veh2x <= vehicle_list[1].edgeimpact_x1) & (impactp_veh2x >= vehicle_list[1].edgeimpact_x2):
            impact[i] = True
            edge_loc[i] = vehicle_list[1].edgeimpact_x1 - impactp_veh2x
            normal_crush[i] = crushdy
    elif vehicle_list[1].edgeimpact == 3:
        crushdx = vehicle_list[1].edgeimpact_x1 - impactp_veh2x
        if (crushdx <= 0) & (impactp_veh2y <= vehicle_list[1].edgeimpact_y1) & (impactp_veh2y >= vehicle_list[1].edgeimpact_y2):
            impact[i] = True
            edge_loc[i] = vehicle_list[1].edgeimpact_y1 - impactp_veh2y
            normal_crush = crushdx
    elif vehicle_list[1].edgeimpact == 4:
        crushdy = vehicle_list[1].edgeimpact_y1 - impactp_veh2y
        if (crushdy < 0) & (impactp_veh2x >= vehicle_list[1].edgeimpact_x1) & (impactp_veh2x <= vehicle_list[1].edgeimpact_x2):
            impact[i] = True
            edge_loc[i] = vehicle_list[1].edgeimpact_x1 - impactp_veh2x
            normal_crush[i] = crushdy

    return crush_data
