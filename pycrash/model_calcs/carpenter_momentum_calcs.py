"""
requires initial position and kinematics of two vehicles
make class that can call this in a loop.
"""


import pandas as pd
import math
import os

def impc(i, vehicle_list, sim_defaults):
    cor = sim_defaults['cor']
    cof = sim_defaults['vehicle_mu']
    veh1 = vehicle_list[0]
    veh2 = vehicle_list[1]

    theta1 = veh1.model.theta_rad[i]   # vehicle 1 heading angle
    dx1 = veh1.model.Dx[i]
    dy1 = veh1.model.Dy[i]
    w1 = veh1.weight
    m1 = w1/32.2
    i1 = veh1.izz
    vx1 = veh.Vx[i]
    vy1 = veh.Vy[i]
    oz_rad1 = veh1['oz_rad']

    # vehicle 2
    theta2 = veh2['theta_rad'] # vehicle 2 heading angle
    dx2 = veh2['dx']
    dy2 = veh2['dy']
    w2 = v_dict2['weight']
    m2 = w2/32.2
    i2 = v_dict2['izz']
    vx2 = veh2['vx']
    vy2 = veh2['vy']
    oz_rad2 = veh2['oz_rad']

    # heading angle of normal impact direction in global frame
    theta_c = veh1.model.theta_rad[i] + veh1.veh.impact_norm_rad
    # carpenter + welcher model

    # get cosine / sine results for coordinate transformation to the normal - tangent axis

    c1 = math.cos(veh1.model.theta_rad[i] - theta_c)
    s1 = math.sin(veh1.model.theta_rad[i] - theta_c)
    c2 = math.cos(veh2.model.theta_rad[i] - theta_c)
    s2 = math.sin(veh2.model.theta_rad[i] - theta_c)

    # translate distances to n-t frame
    dt1 = c1*veh1.model.Dx[i] - s1*veh1.model.Dy[i]
    dn1 = s1*veh1.model.Dx[i] + c1*veh1.model.Dy[i]
    dt2 = c2*veh2.model.Dx[i] - s2*veh2.model.Dy[i]
    dn2 = s2*veh2.model.Dx[i] + c2*veh2.model.Dy[i]

    # translate velocities to n-t frame
    vt1 = c1*veh1.model.Vx[i] - s1*veh1.model.Vy[i]
    vn1 = s1*veh1.model.Vx[i] + c1*veh1.model.Vy[i]
    vt2 = c2*veh2.model.Vx[i] - s2*veh2.model.Vy[i]
    vn2 = s2*veh2.model.Vx[i] + c2*veh2.model.Vy[i]

    # pre-impact POI velocities (Equations 1)
    vct1 = vt1 - dn1*veh1.model.oz_rad[i]
    vct2 = vt2 - dn2*veh2.model.oz_rad[i]
    vct21 = vct2 - vct1

    vcn1 = vn1 + dt1*oz_rad1
    vcn2 = vn2 + dt2*oz_rad2
    vcn21 = vcn2 - vcn1

    A11 = (1 / (veh1.weight / 32.2) + 1 / (veh2.weight / 32.2) + dn1**2 / veh1.izz + dn2**2 / veh2.izz)
    A12 = (dt1 * dn1 / veh1.izz + dt2 * dn2 / veh2.izz)
    A22 = (1 / (veh1.weight / 32.2) + 1 / (veh2.weight / 32.2) + dt1**2 / veh1.izz + dt2**2 / veh2.izz)
    A = (A11 * A22 - A12 * A12)

    # collision impulse -
    pt = (1+cor) * (A22 * vct21 + A12 * vcn21) / A
    pn = (1+cor) * (A12 * vct21 + A11 * vcn21) / A

    p_ratio = abs(pt/pn)   # equation 10
    alpha = 1

    if p_ratio > cof:
            print('Sliding Condition')
            pn_s = (1+cor) * vcn21 / (A22 - alpha * cof * A12)
            pt_s = alpha * cof * pn_s

            if pt * pt_s > 0:           # test for sliding direction
                pt = pt_s               # alpha = 1 is correct, keep initial try
                pn = pn_s
            else:
                alpha = -1
                pn = (1+cor) * vcn21 / (A22 - alpha * cof * A12)   # sliding in wrong direction, alpha = -1
                pt = alpha * cof * pn
    else:
        print ('No Sliding')                                                      # no sliding, original pt, pn are correct

    if pn * dn1 < 0:
        print('Compression')
    else:
        print('Tension')

    # change in velocity in collision frame
    # Equation 16 - termination of restitution

    dvt1 = pt / m1
    dvn1 = pn / m1
    doz1 = (-1*dn1 * pt + dt1 * pn) / i1

    dvt2 = -1 * pt / m2
    dvn2 = -1 * pn / m2
    doz2 = (dn2 * pt - dt2 * pn) / i2

    # tranform back to local vehicle coordinate system
    # delta-Vs
    dvx1 = (c1*dvt1 + s1*dvn1) / 1.46667
    dvy1 = (-1*s1*dvt1 + c1*dvn1) / 1.46667
    dveh1 = math.sqrt(dvx1**2 + dvy1**2)
    doz1_deg = doz1 * 180 / math.pi

    dvx2 = (c2*dvt2 + s2*dvn2) / 1.46667
    dvy2 = (-1*s2*dvt2 + c2*dvn2) / 1.46667
    dveh2 = math.sqrt(dvx2**2 + dvy2**2)
    doz2_deg = doz2 * 180 / math.pi

    # post impact speeds
    vx1_ = vx1 / 1.46667 + dvx1
    vy1_ = vy1 / 1.46667 + dvy1
    veh1_ = math.sqrt(vx1_**2 + vy1_**2)
    oz_deg1_ = oz_rad1 * 180 / math.pi + doz1_deg
    oz_rad1_ = oz_deg1_ * math.pi / 180

    vx2_ = vx2 / 1.46667 + dvx2
    vy2_ = vy2 / 1.46667 + dvy2
    veh2_ = math.sqrt(vx2_**2 + vy2_**2)
    oz_deg2_ = oz_rad2 * 180 / math.pi + doz2_deg
    oz_rad2_ = oz_deg2_ * math.pi / 180

    # calculations for energy dissipated
    vmt1 = vt1 + dvt1 / (1 + cor)
    omgm1 = oz_rad1 + doz1 / (1 + cor)
    vmt2 = vt2 + dvt2 / (1 + cor)
    omgm2 = oz_rad2 + doz2 / (1 + cor)

    vmct21 = vmt2 - vmt1 - dn2 * omgm2 + dn1 * omgm1

    if vmct21 * vct21 < 0:
        print('Reverse Slide')
    else:
        print('Forward Slide')

    vt1_ = vt1 + dvt1
    vt2_ = vt2 + dvt2
    vct21_ = vt2_ - dn2 * oz_rad2_ - vt1_ + dn1 * oz_rad1_

    vn1_ = vn1 + dvn1
    vn2_ = vn2 + dvn2
    vcn21_ = vn2_ + dt2 * oz_rad2_ - vn1_ - dt1 * oz_rad1_

    # dissipated energies
    ke_surface_dis = pt * vmct21
    ke_volume_dis = 0.5 * (1-cor) * (pt * (vct21 - vmct21) + pn * vcn21)
    ke_total_dis = ke_surface_dis + ke_volume_dis

    ke_volume_abs = 0.5 / (1+cor) * (pt * (vct21 - vmct21) + pn * vcn21)
    ke_total_abs = 0.5 / (1+cor) * (pt * (vct21 + vmct21) + pn * vcn21)

    t_effects_dis = 0.5 * pt * (vct21 + vct21_)
    n_effects_dis = 0.5 * pn * (vcn21 + vcn21_)
    tn_total_dis = t_effects_dis + n_effects_dis

    #veh1_imp = {'vx': vx1_* 1.46667, 'vy': vy1_* 1.46667, 'oz_rad': oz_rad1_, 'dvx':dvx1* 1.46667, 'dvy': dvy1* 1.46667, 'dv':dveh1* 1.46667}
    #veh2_imp = {'vx': vx2_* 1.46667, 'vy': vy2_* 1.46667, 'oz_rad': oz_rad2_, 'dvx':dvx2* 1.46667, 'dvy': dvy2* 1.46667, 'dv':dveh2* 1.46667}

    # speeds in mph -
    veh1.impc_result = {'vx_post': vx1_, 'vy_post': vy1_, 'oz_rad_post': oz_rad1_, 'dvx':dvx1, 'dvy': dvy1, 'dv':dveh1}
    veh2.impc_result = {'vx_post': vx2_, 'vy_post': vy2_, 'oz_rad_post': oz_rad2_, 'dvx':dvx2, 'dvy': dvy2, 'dv':dveh2}
    impc_energy = {'t_effects_dis':t_effects_dis, 'n_effects_dis':n_effects_dis, 'tn_total_dis':tn_total_dis}

    return vehicle_list, impc_energy
