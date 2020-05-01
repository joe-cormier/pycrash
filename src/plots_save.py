# -*- coding: utf-8 -*-
"""
Created on Mon May 13 21:58:23 2019

@author: JCormier
"""
# Contains all functions used to plot various elements of the program

import matplotlib.pyplot as plt

def plot_inputs(df_in):
    fig, axs = plt.subplots(1, 2, figsize=(16,6), sharey=False)
    axs[0].set_xlabel('time (s)')
    axs[0].set_ylabel('Input Velocity (mph), Input Angular Rate (deg/s)', color='k')
    axs[0].plot(df_in.t, df_in.v_edr, color='k')
    axs[0].plot(df_in.t, df_in.oz, color='g')
    axs[0].tick_params(axis='y', labelcolor='k')

    axs[1].set_xlabel('time (s)')
    axs[1].set_ylabel('Input Steering Wheel Angle (deg), Input Throttle (%)', color='k')
    axs[1].tick_params(axis='y', labelcolor='k')
    axs[1].plot(df_in.t, df_in.sw_angle, color='k')
    axs[1].plot(df_in.t, df_in.throttle_edr, color='r')

    ax2 = []
    ax2.append(axs[0].twinx())
    ax2[0].set_ylabel('Input Derived Acceleration (g)', color='b')
    ax2[0].plot(df_in.t, df_in.a_edr/32.2, color='b')
    ax2[0].tick_params(axis='y', labelcolor='b')

    ax2.append(axs[1].twinx())
    ax2[1].plot(df_in.t, df_in.brake, color='b')
    ax2[1].tick_params(axis='y', labelcolor='b')
    ax2[1].set_ylabel('Input Brake', color='b')

    plt.subplots_adjust(wspace=0.6)
    plt.show()

def plot_vehicle_pre_motion(pre_df):
    fig, axs = plt.subplots(1, 2, figsize=(16,6), sharey=False)
    axs[0].set_xlabel('time (s)')
    axs[0].set_ylabel('Velocity (mph) (vx, vy)', color='k')
    axs[0].plot(pre_df.t, pre_df.vx, color='k')
    axs[0].plot(pre_df.t, pre_df.vy, color='g')
    axs[0].tick_params(axis='y', labelcolor='b')

    axs[1].set_xlabel('time (s)')
    axs[1].set_ylabel('Acceleration (g)', color='k')
    axs[1].tick_params(axis='y', labelcolor='k')
    axs[1].plot(pre_df.t, pre_df.ax/32.2, color='g')
    axs[1].plot(pre_df.t, pre_df.ay/32.2, color='b')

    #ax2 = []
    #ax2.append(axs[0].twinx())
    #ax2[0].set_ylabel('Acceleration (g) (ax, ay)', color='b')
    #ax2[0].plot(pre_df.t, pre_df.ax/32.2, color='b')
    #ax2[0].plot(pre_df.t, pre_df.ax/32.2, color='r')
    #ax2[0].tick_params(axis='y', labelcolor='b')

    #ax2.append(axs[1].twinx())
    #ax2[1].plot(df_in.t, df_in.brake_edr, color='b')
    #ax2[1].tick_params(axis='y', labelcolor='b')
    #ax2[1].set_ylabel('EDR Brake', color='b')

    plt.subplots_adjust(wspace=0.6)
    plt.show()

def draw_vehicle(draw_vx, draw_vy, i):
    #  These dataframes link the components together for plotting
    bdy_x = (draw_vx.b_lfc[i], draw_vx.b_rfc[i], draw_vx.b_rrc[i], draw_vx.b_lrc[i], draw_vx.b_lfc[i])
    bdy_y = (draw_vy.b_lfc[i], draw_vy.b_rfc[i], draw_vy.b_rrc[i], draw_vy.b_lrc[i], draw_vy.b_lfc[i])

    lfw_x = (draw_vx.lfw_a[i], draw_vx.lfw_b[i], draw_vx.lfw_c[i], draw_vx.lfw_d[i], draw_vx.lfw_a[i])
    lfw_y = (draw_vy.lfw_a[i], draw_vy.lfw_b[i], draw_vy.lfw_c[i], draw_vy.lfw_d[i], draw_vy.lfw_a[i])

    rfw_x = (draw_vx.rfw_a[i], draw_vx.rfw_b[i], draw_vx.rfw_c[i], draw_vx.rfw_d[i], draw_vx.rfw_a[i])
    rfw_y = (draw_vy.rfw_a[i], draw_vy.rfw_b[i], draw_vy.rfw_c[i], draw_vy.rfw_d[i], draw_vy.rfw_a[i])

    rrw_x = (draw_vx.rrw_a[i], draw_vx.rrw_b[i], draw_vx.rrw_c[i], draw_vx.rrw_d[i], draw_vx.rrw_a[i])
    rrw_y = (draw_vy.rrw_a[i], draw_vy.rrw_b[i], draw_vy.rrw_c[i], draw_vy.rrw_d[i], draw_vy.rrw_a[i])

    lrw_x = (draw_vx.lrw_a[i], draw_vx.lrw_b[i], draw_vx.lrw_c[i], draw_vx.lrw_d[i], draw_vx.lrw_a[i])
    lrw_y = (draw_vy.lrw_a[i], draw_vy.lrw_b[i], draw_vy.lrw_c[i], draw_vy.lrw_d[i], draw_vy.lrw_a[i])

    #%% Plot Vehicle in Vehicle reference frame
    plt.figure(figsize=(16,9))
    plt.xlim([-20, 20])
    plt.ylim([-10, 10])

    plt.plot(bdy_x, bdy_y, 'k')
    plt.scatter(draw_vx.lfw[i], draw_vy.lfw[i], c='b')         # left front wheel center
    plt.plot(lfw_x, lfw_y, 'b')
    plt.scatter(draw_vx.rfw[i], draw_vy.rfw[i], c='g')       # right front wheel center
    plt.plot(rfw_x, rfw_y, 'g')
    plt.scatter(draw_vx.rrw[i], draw_vy.rrw[i],c='m')       # right rear wheel center
    plt.plot(rrw_x, rrw_y,'m')
    plt.scatter(draw_vx.lrw[i], draw_vy.lrw[i], c='r')       # left rear wheel center
    plt.plot(lrw_x, lrw_y, 'r')

    # vehicle CG
    plt.scatter(draw_vx.cg[i], draw_vy.cg[i],s=500, c='k')

    # velocity vector

    plt.arrow(draw_vx.cg[i], draw_vy.cg[i], draw_vx.vel_v[i]-draw_vx.cg[i], draw_vy.vel_v[i]-draw_vy.cg[i], head_width=.5, head_length=0.5, fc='k', ec='k')

    # vehicle axes
    plt.arrow(draw_vx.cg[i], draw_vy.cg[i], draw_vx.xaxis[i]-draw_vx.cg[i], draw_vy.xaxis[i]-draw_vy.cg[i], head_width=.5, head_length=0.5, fc='r', ec='r')
    plt.arrow(draw_vx.cg[i], draw_vy.cg[i], draw_vx.yaxis[i]-draw_vx.cg[i], draw_vy.yaxis[i]-draw_vy.cg[i], head_width=.5, head_length=0.5, fc='b', ec='b')
    plt.gca().invert_yaxis()
    plt.show()

def draw_vehicle_motion(draw_gx, draw_gy, i):
    #%% Plot Vehicle in Global reference frame

    bdy_x = (draw_gx.b_lfc[i], draw_gx.b_rfc[i], draw_gx.b_rrc[i], draw_gx.b_lrc[i], draw_gx.b_lfc[i])
    bdy_y = (draw_gy.b_lfc[i], draw_gy.b_rfc[i], draw_gy.b_rrc[i], draw_gy.b_lrc[i], draw_gy.b_lfc[i])

    lfw_x = (draw_gx.lfw_a[i], draw_gx.lfw_b[i], draw_gx.lfw_c[i], draw_gx.lfw_d[i], draw_gx.lfw_a[i])
    lfw_y = (draw_gy.lfw_a[i], draw_gy.lfw_b[i], draw_gy.lfw_c[i], draw_gy.lfw_d[i], draw_gy.lfw_a[i])

    rfw_x = (draw_gx.rfw_a[i], draw_gx.rfw_b[i], draw_gx.rfw_c[i], draw_gx.rfw_d[i], draw_gx.rfw_a[i])
    rfw_y = (draw_gy.rfw_a[i], draw_gy.rfw_b[i], draw_gy.rfw_c[i], draw_gy.rfw_d[i], draw_gy.rfw_a[i])

    rrw_x = (draw_gx.rrw_a[i], draw_gx.rrw_b[i], draw_gx.rrw_c[i], draw_gx.rrw_d[i], draw_gx.rrw_a[i])
    rrw_y = (draw_gy.rrw_a[i], draw_gy.rrw_b[i], draw_gy.rrw_c[i], draw_gy.rrw_d[i], draw_gy.rrw_a[i])

    lrw_x = (draw_gx.lrw_a[i], draw_gx.lrw_b[i], draw_gx.lrw_c[i], draw_gx.lrw_d[i], draw_gx.lrw_a[i])
    lrw_y = (draw_gy.lrw_a[i], draw_gy.lrw_b[i], draw_gy.lrw_c[i], draw_gy.lrw_d[i], draw_gy.lrw_a[i])


    plt.figure(figsize=(10,10))
    #plt.xlim([-40, 80])
    #plt.ylim([-40, 40])

    plt.plot(bdy_x, bdy_y, 'k')
    plt.scatter(draw_gx.lfw[i], draw_gy.lfw[i], c='b')       # left front wheel center
    plt.plot(lfw_x, lfw_y, 'b')
    plt.scatter(draw_gx.rfw[i], draw_gy.rfw[i], c='g')       # right front wheel center
    plt.plot(rfw_x, rfw_y, 'g')
    plt.scatter(draw_gx.rrw[i], draw_gy.rrw[i], c='m')       # right rear wheel center
    plt.plot(rrw_x, rrw_y,'m')
    plt.scatter(draw_gx.lrw[i], draw_gy.lrw[i], c='r')       # left rear wheel center
    plt.plot(lrw_x, lrw_y, 'r')
    plt.scatter(draw_gx.cg[i], draw_gy.cg[i],s=200, c='k')                                # vehicle CG
    plt.arrow(draw_gx.cg[i], draw_gy.cg[i], draw_gx.vel_v[i]-draw_gx.cg[i], draw_gy.vel_v[i]-draw_gy.cg[i], head_width=.5, head_length=0.5, fc='k', ec='k')     # velocity vector
    plt.arrow(draw_gx.cg[i], draw_gy.cg[i], draw_gx.xaxis[i]-draw_gx.cg[i], draw_gy.xaxis[i]-draw_gy.cg[i], head_width=.5, head_length=0.5, fc='r', ec='r')     # vehicle axes
    plt.arrow(draw_gx.cg[i], draw_gy.cg[i], draw_gx.yaxis[i]-draw_gx.cg[i], draw_gy.yaxis[i]-draw_gy.cg[i], head_width=.5, head_length=0.5, fc='b', ec='b')     # vehicle axes
    plt.gca().invert_yaxis()
    plt.show()
