"""
create a collision plane on the striking vehicle
this will indicate the contact point and direction of the nornmal and tangential axis of impact force / momentum balance
"""
from pycrash.visualization.vehicle import plot_impact_points, plot_impact_edge
import math

def define_impact_plane(veh, iplane = True):
    """
    generates a point in vehicle 1 (striking) reference frame
    sideswipe collisions - px, py will determine the extent of vehcle engagement with respect
    to contacting edge in vehicle 2 (struck)
    impact momentum model - px, py will be used along with the impact plane to determine time
    of impact and direction of normal and tangential contact planes
    when plane = True, user will also indicate direction of normal impact plane
    """
    user_loc = False
    # set impact edge to zero
    veh.striking = True

    # test for required inputs
    if not veh.lcgf:
        veh.lcgf = float(input("Enter CG to front axle (ft)"))

    if not veh.lcgr:
        veh.lcgr = float(input("Enter CG to rear axle (ft)"))

    if not veh.f_hang:
        veh.f_hang = float(input("Enter front overhang (ft)"))

    if not veh.r_hang:
        veh.r_hang = float(input("Enter rear overhang (ft)"))

    if not veh.width:
        veh.width = float(input("Enter vehicle width (ft)"))

    # create figure of vehicle 1 with scale / grid and p1, p2, p3, p4 labeled when function is called
    # option 5 = custom location
    plot_impact_points(veh, iplane = False) # plot vehicle points

    impact_option = int(input("Choose option for impact point (1, 2, 3, 4, custom = 99: "))

    if impact_option not in [1, 2, 3, 4, 99]:
        print("Invalid impact point option - enter 1, 2, 3, 4 or 5")
        impact_option = int(input("Choose option for impact location"))
    elif impact_option != 99:
        if impact_option == 1:
            veh.pimpact_x = veh.lcgf + veh.f_hang
            veh.pimpact_y = -1 * veh.width / 2
        elif impact_option == 2:
            veh.pimpact_x = veh.lcgf + veh.f_hang
            veh.pimpact_y = veh.width / 2
        elif impact_option == 3:
            veh.pimpact_x = -1 * veh.lcgr - veh.r_hang
            veh.pimpact_y = veh.width / 2
        elif impact_option == 4:
            veh.pimpact_x = -1 * veh.lcgr - veh.r_hang
            veh.pimpact_y = -1* veh.width / 2
    elif impact_option == 99:
        veh.pimpact_x = float(input("Enter x-coordinate ( + forward) of impact point in vehicle frame (ft):"))
        veh.pimpact_y = float(input("Enter y-coordinate ( + rightward) of impact point in vehicle frame (ft):"))
        user_loc = True

    if iplane:
        veh.impact_norm_rad = float(input("Enter heading angle of normal impact plane:  ")) * math.pi / 180
        norm_length = veh.width
        tang_length = veh.width / 2

        veh.impact_norm_x = veh.pimpact_x + norm_length * math.cos(veh.impact_norm_rad)
        veh.impact_norm_y = veh.pimpact_y + norm_length * math.sin(veh.impact_norm_rad)

        veh.impact_tang_x = veh.pimpact_x + tang_length * math.cos(veh.impact_norm_rad + math.pi / 2)
        veh.impact_tang_y = veh.pimpact_y + tang_length * math.sin(veh.impact_norm_rad + math.pi / 2)

    plot_impact_points(veh, user_loc) # plot vehicle points

    return veh

def define_impact_edge(veh, iplane = False):
    """
    generates an edge in vehicle 2 (struck) reference frame
    sideswipe collisions - edge will determine the extent of vehcle engagement with respect
    to contacting point in vehicle 1 (striking)
    impact momentum model - impact edge will be used along with the impact plane to determine time
    of impact
    """
    veh.striking = False

    # test for required inputs
    if not veh.lcgf:
        veh.lcgf = float(input("Enter CG to front axle (ft)"))

    if not veh.lcgr:
        veh.lcgr = float(input("Enter CG to rear axle (ft)"))

    if not veh.f_hang:
        veh.f_hang = float(input("Enter front overhang (ft)"))

    if not veh.r_hang:
        veh.r_hang = float(input("Enter rear overhang (ft)"))

    if not veh.width:
        veh.width = float(input("Enter vehicle width (ft)"))

    # create figure of vehicle 1 with scale / grid and p1, p2, p3, p4 labeled when function is called
    # option 5 = custom location

    plot_impact_edge(veh)

    impact_option = int(input("Choose option for impact edge: "))

    if impact_option not in [1, 2, 3, 4]:
        raise ValueError("Invalid impact edge option - enter 1, 2, 3, 4")
    else:
        if impact_option == 1:
            veh.edgeimpact = 1
            veh.edgeimpact_x1 = veh.lcgf + veh.f_hang
            veh.edgeimpact_y1 = -1 * veh.width / 2
            veh.edgeimpact_x2 = veh.lcgf + veh.f_hang
            veh.edgeimpact_y2 = veh.width / 2
        elif impact_option == 2:
            veh.edgeimpact = 2
            veh.edgeimpact_x1 = veh.lcgf + veh.f_hang
            veh.edgeimpact_y1 = veh.width / 2
            veh.edgeimpact_x2 = -1 * veh.lcgr - veh.r_hang
            veh.edgeimpact_y2 = veh.width / 2
        elif impact_option == 3:
            veh.edgeimpact = 3
            veh.edgeimpact_x1 = -1 * veh.lcgr - veh.r_hang
            veh.edgeimpact_y1 = veh.width / 2
            veh.edgeimpact_x2 = -1 * veh.lcgr - veh.r_hang
            veh.edgeimpact_y2 = -1* veh.width / 2
        elif impact_option == 4:
            veh.edgeimpact = 4
            veh.edgeimpact_x1 = -1 * veh.lcgr - veh.r_hang
            veh.edgeimpact_y1 = -1 * veh.width / 2
            veh.edgeimpact_x2 = veh.lcgf + veh.f_hang
            veh.edgeimpact_y2 = -1 * veh.width / 2

    return veh
