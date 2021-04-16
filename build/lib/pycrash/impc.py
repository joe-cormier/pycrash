import numpy as np

def impc_calcs(veh1, veh2, poi_veh2x, poi_veh2y, sim_inputs):
    cor = sim_inputs['cor']
    cof = abs(sim_inputs['cof'])
    impact_norm_deg = sim_inputs['impact_norm_deg']
    # heading angle [rad] of tangent impact direction in global frame
    theta_c = (veh1.head_angle * np.pi / 180) + (impact_norm_deg * np.pi / 180) + (90 / 180 * np.pi)
    print(f'theta c: {theta_c * 180 / np.pi:0.2f} [deg]')

    # carpenter + welcher model
    # get cosine / sine results for coordinate transformation to the normal - tangent axis
    c1 = np.cos(veh1.head_angle * np.pi / 180 - theta_c)
    s1 = np.sin(veh1.head_angle * np.pi / 180 - theta_c)
    c2 = np.cos(veh2.head_angle * np.pi / 180 - theta_c)
    s2 = np.sin(veh2.head_angle * np.pi / 180 - theta_c)

    # translate distances to n-t frame
    dt1 = c1*(veh1.pimpact_x) - s1*(veh1.pimpact_y)
    dn1 = s1*(veh1.pimpact_x) + c1*(veh1.pimpact_y)
    dt2 = c2*(poi_veh2x) - s2*(poi_veh2y)
    dn2 = s2*(poi_veh2x) + c2*(poi_veh2y)

    # translate velocities to n-t frame
    vt1 = c1*veh1.vx_initial - s1*veh1.vy_initial
    vn1 = s1*veh1.vx_initial + c1*veh1.vy_initial
    vt2 = c2*veh2.vx_initial - s2*veh2.vy_initial
    vn2 = s2*veh2.vx_initial + c2*veh2.vy_initial

    # pre-impact POI velocities (Equations 1)
    vct1 = vt1 - dn1 * veh1.omega_z * np.pi / 180
    vct2 = vt2 - dn2 * veh2.omega_z * np.pi / 180
    vct21 = vct2 - vct1

    vcn1 = vn1 + dt1 * veh1.omega_z * np.pi / 180
    vcn2 = vn2 + dt2 * veh2.omega_z * np.pi / 180
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
    print(f'p-ratio: {p_ratio:0.2f}, cof: {cof}')
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

    dvt1 = pt / (veh1.weight/32.2)
    dvn1 = pn / (veh1.weight/32.2)
    doz1 = (-1*dn1 * pt + dt1 * pn) / veh1.izz

    dvt2 = -1 * pt / (veh2.weight/32.2)
    dvn2 = -1 * pn / (veh2.weight/32.2)
    doz2 = (dn2 * pt - dt2 * pn) / veh2.izz

    # transform back to local vehicle coordinate system
    # delta-Vs
    dvx1 = (c1*dvt1 + s1*dvn1)
    dvy1 = (-1*s1*dvt1 + c1*dvn1)
    dveh1 = np.sqrt(dvx1**2 + dvy1**2)
    doz1_deg = doz1 * 180 / np.pi

    dvx2 = (c2*dvt2 + s2*dvn2)
    dvy2 = (-1*s2*dvt2 + c2*dvn2)
    dveh2 = np.sqrt(dvx2**2 + dvy2**2)
    doz2_deg = doz2 * 180 / np.pi

    # post impact speeds
    vx1_ = veh1.vx_initial + dvx1
    vy1_ = veh1.vy_initial + dvy1
    veh1_ = np.sqrt(vx1_**2 + vy1_**2)
    oz_deg1_ = veh1.omega_z + doz1_deg
    oz_rad1_ = oz_deg1_ * np.pi / 180

    vx2_ = veh2.vx_initial + dvx2
    vy2_ = veh2.vy_initial + dvy2
    veh2_ = np.sqrt(vx2_**2 + vy2_**2)
    oz_deg2_ = veh2.omega_z + doz2_deg
    oz_rad2_ = oz_deg2_ * np.pi / 180

    # calculations for energy dissipated
    vmt1 = vt1 + dvt1 / (1 + cor)
    omgm1 = veh1.omega_z + doz1 / (1 + cor)
    vmt2 = vt2 + dvt2 / (1 + cor)
    omgm2 = veh2.omega_z + doz2 / (1 + cor)

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

    # speeds in mph -
    veh1_imp = {'vx': vx1_* 0.681818, 'vy': vy1_* 0.681818, 'oz_rad': oz_rad1_, 'oz_deg': oz_deg1_, 'dvx':dvx1 * 0.681818, 'dvy': dvy1 * 0.681818, 'dv':dveh1 * 0.681818}
    veh2_imp = {'vx': vx2_* 0.681818, 'vy': vy2_* 0.681818, 'oz_rad': oz_rad2_, 'oz_deg': oz_deg2_, 'dvx':dvx2 * 0.681818, 'dvy': dvy2 * 0.681818, 'dv':dveh2 * 0.681818}


    #veh1.impc_result = {'vx_post': vx1_, 'vy_post': vy1_, 'oz_rad_post': oz_rad1_, 'dvx':dvx1, 'dvy': dvy1, 'dv':dveh1}
    #veh2.impc_result = {'vx_post': vx2_, 'vy_post': vy2_, 'oz_rad_post': oz_rad2_, 'dvx':dvx2, 'dvy': dvy2, 'dv':dveh2}
    impc_energy = {'t_effects_dis': t_effects_dis, 'n_effects_dis':n_effects_dis, 'tn_total_dis':tn_total_dis}

    print(f'Impact Energy: {impc_energy}')
    return veh1_imp, veh2_imp
