"""
functions for detecting impact using point (Veh1) and edge (Veh2)
"""

def impact_dect(vehicle_list):
    # TODO: assuming that vehicle_list = [veh1, veh2] - can fix by checking for impact point definition

    # current location of impact point
    cgx1 = vehicle_list[1].veh_model.v_model.Dx.iloc[-1]
    cgy1 = vehicle_list[1].veh_model.v_model.Dy.iloc[-1]
    theta_rad1 = vehicle_list[1].veh_model.v_model.theta_rad.iloc[-1]

    impactp_gx = cgx1 + vehicle_list[1].veh.pimpact_x * math.cos(theta_rad1) - vehicle_list[1].veh.pimpact_y * math.sin(theta_rad1)
    impactp_gy = cgy1 + vehicle_list[1].veh.pimpact_x * math.sin(theta_rad1) + vehicle_list[1].veh.pimpact_y * math.cos(theta_rad1)

    # impact plane
    cgx2 = vehicle_list[2].veh_model.v_model.Dx.iloc[-1]
    cgy2 = vehicle_list[2].veh_model.v_model.Dy.iloc[-1]
    theta_rad2 = vehicle_list[2].veh_model.v_model.theta_rad.iloc[-1]

    # impact point in veh2 reference frame
    impactp_veh2x = impactp_gx * math.cos(theta_rad2) + impactp_gy * math.sin(theta_rad2)
    impactp_veh2y = -1 * impactp_gy * math.sin(theta_rad2) + impactp_gy * math.cos(theta_rad2)

    edgeimpact_x1 = cgx2 + vehicle_list[1].veh.edgeimpact_x1 * math.cos(theta_rad1) - vehicle_list[1].veh.edgeimpact_y1 * math.sin(theta_rad1)
    edgeimpact_y1 = cgy2 + vehicle_list[1].veh.edgeimpact_x1 * math.sin(theta_rad1) + vehicle_list[1].veh.edgeimpact_y1 * math.cos(theta_rad1)
    edgeimpact_x2 = cgx2 + vehicle_list[1].veh.edgeimpact_x2 * math.cos(theta_rad1) - vehicle_list[1].veh.edgeimpact_y2 * math.sin(theta_rad1)
    edgeimpact_y2 = cgy2 + vehicle_list[1].veh.edgeimpact_x2 * math.sin(theta_rad1) + vehicle_list[1].veh.edgeimpact_y2 * math.cos(theta_rad1)

    impact = 0
    crushdx = 0
    crushdy = 0

    if vehicle_list[2].edgeimpact == 1:
        crushdx = impactp_veh2x - edgeimpact_x1
        if (crushdx <= 0) & (impactp_veh2y > edgeimpact_y1) & (impactp_veh2y < edgeimpact_y2):
            impact = 1
            crushdy = impactp_veh2y
    elif vehicle_list[2].edgeimpact == 2:
        crushdy = impactp_veh2y - edgeimpact_y1
        if (crushdy <= 0) & (impactp_veh2x < edgeimpact_x1) & (impactp_veh2x > edgeimpact_x2):
            impact = 1
            crushdx = impactp_veh2x
    elif vehicle_list[2].edgeimpact == 3:
        crushdx = edgeimpact_x1 - impactp_veh2x
        if (crushdx <= 0) & (impactp_veh2y > edgeimpact_y1) & (impactp_veh2y < edgeimpact_y2):
            impact = 1
            crushdy = impactp_veh2y
    elif vehicle_list[2].edgeimpact == 4:
        crushdy = edgeimpact_y1 - impactp_veh2y
        if (crushdy <= 0) & (impactp_veh2x < edgeimpact_x1) & (impactp_veh2x > edgeimpact_x2):
            impact = 1
            crushdx = impactp_veh2x

    return {'impact':impact, 'crushdx':crushdx, 'crushdy':crushdy}
