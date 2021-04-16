"""
create a collision plane on the striking vehicle
this will indicate the contact point and direction of the nornmal and tangential axis of impact force / momentum balance
"""
from pycrash.visualization.vehicle import plot_impact_points, plot_impact_edge
import math

def define_impact_plane(veh, iplane=True):
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
    plot_impact_points(veh, iplane=False)  # plot vehicle points

    veh.impact_points = []  # list of impact points x, y and normal impact plane angle deg
    veh.impact_norm = []    # list of points for plotting the impact plane
    veh.impact_tang = []    # list of points for plotting the impact plane

    """ create list of impact points - this will be a list of tuples"""
    for i in range(0, veh.impactTotal):
        impact_option = int(input("Choose option for impact point (1, 2, 3, 4, custom = 99: "))

        if impact_option not in [1, 2, 3, 4, 99]:
            print("Invalid impact point option - enter 1, 2, 3, 4 or 5")
            impact_option = int(input("Choose option for impact location"))
        elif impact_option != 99:
            if impact_option == 1:
                veh.impact_points.append((veh.lcgf + veh.f_hang, -1 * veh.width / 2))
            elif impact_option == 2:
                veh.impact_points.append((veh.lcgf + veh.f_hang, veh.width / 2))
            elif impact_option == 3:
                veh.impact_points.append((-1 * veh.lcgr - veh.r_hang, veh.width / 2))
            elif impact_option == 4:
                veh.impact_points.append((-1 * veh.lcgr - veh.r_hang, -1 * veh.width / 2))
        elif impact_option == 99:
            veh.impact_points.append((float(input("Enter x-coordinate ( + forward) of impact point in vehicle frame (ft):")),
                                      float(input("Enter y-coordinate ( + rightward) of impact point in vehicle frame (ft):"))))
            user_loc = True

        if iplane:
            veh.impact_points[i] += (float(input("Enter heading angle of normal impact plane (deg):  ")), )  # append to x,y cooridinates
            norm_length = veh.width
            tang_length = veh.width / 2

            veh.impact_norm.append((veh.impact_points[i][0] + norm_length * math.cos(veh.impact_points[i][2] * math.pi / 180),
                                  veh.impact_points[i][1] + norm_length * math.sin(veh.impact_points[i][2] * math.pi / 180)))

            veh.impact_tang.append((veh.impact_points[i][0] + tang_length * math.cos(veh.impact_points[i][2] * math.pi / 180 + math.pi / 2),
                                  veh.impact_points[i][1] + tang_length * math.sin(veh.impact_points[i][2] * math.pi / 180 + math.pi / 2)))

        print(veh.impact_points)
        plot_impact_points(veh)  # plot vehicle points

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


    veh.edgeimpact_points = []   # store x,y values for edge points - moving clockwise
    veh.edgeimpact = []    # defines location of edge

    plot_impact_edge(veh)


    for i in range(0, veh.impactTotal):
        impact_option = int(input("Choose impact edge for the corresponding impact point on striking vehicle: "))

        if impact_option not in [0, 1, 2, 3]:
            raise ValueError("Invalid impact edge option - enter 0, 1, 2, 3")
        else:
            if impact_option == 0:
                veh.edgeimpact.append(0)
                veh.edgeimpact_points.append((veh.lcgf + veh.f_hang, -1 * veh.width / 2,
                                              veh.lcgf + veh.f_hang, veh.width / 2))
            elif impact_option == 1:
                veh.edgeimpact.append(1)
                veh.edgeimpact_points.append((veh.lcgf + veh.f_hang, veh.width / 2,
                                              -1 * veh.lcgr - veh.r_hang, veh.width / 2))
            elif impact_option == 2:
                veh.edgeimpact.append(2)
                veh.edgeimpact_points.append((-1 * veh.lcgr - veh.r_hang, veh.width / 2,
                                              -1 * veh.lcgr - veh.r_hang, -1 * veh.width / 2))
            elif impact_option == 3:
                veh.edgeimpact.append(3)
                veh.edgeimpact_points.append((-1 * veh.lcgr - veh.r_hang, -1 * veh.width / 2,
                                              veh.lcgf + veh.f_hang, -1 * veh.width / 2))

    return veh
