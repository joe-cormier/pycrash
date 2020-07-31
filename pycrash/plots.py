# -*- coding: utf-8 -*-
"""
Created on Mon May 13 21:58:23 2019

@author: JCormier
"""
# Contains all functions used to plot various elements of the program

import matplotlib.pyplot as plt
import numpy as np
import math

def plot_inputs(df_in):
    fig, axs = plt.subplots(2, 2, figsize=(18,10), sharey=False)
    axs[0,0].set_xlabel('time (s)')
    axs[0,0].set_title('EDR Speed, Angular Rate, Derived Acceleration', color='k')
    axs[0,0].plot(df_in.t, df_in.v_edr / 1.46667, color='k')
    axs[0,0].plot(df_in.t, df_in.oz_edr, color='g')
    axs[0,0].tick_params(axis='y', labelcolor='k')
    axs[0,0].set_ylabel('Velocity (mph) | Angular Rate (deg/s)', color='k')

    ax2 = []
    ax2.append(axs[0,0].twinx())
    ax2[0].set_ylabel('Derived Acceleration (g)', color='r')
    ax2[0].plot(df_in.t, df_in.a_edr/32.2, color='r')
    ax2[0].tick_params(axis='y', labelcolor='r')

    axs[0,1].set_xlabel('time (s)')
    axs[0,1].set_title('EDR Steering, Brake and Throttle', color='k')
    axs[0,1].tick_params(axis='y', labelcolor='k')
    axs[0,1].plot(df_in.t, df_in.sw_angle_edr, color='k')
    axs[0,1].plot(df_in.t, df_in.throttle_edr, color='r')
    axs[0,1].set_ylabel('Steering Wheel Angle (deg) | Throttle (%)', color='k')

    ax2.append(axs[0,1].twinx())
    ax2[1].plot(df_in.t, df_in.brake_edr, color='b')
    ax2[1].tick_params(axis='y', labelcolor='b')
    ax2[1].set_ylabel('Brake Status', color='b')

    axs[1,0].set_xlabel('time (s)')
    axs[1,0].set_title('Calculated Velocity (mph), Angular Rate (deg/s)', color='k')
    ax2.append(axs[1,0].twinx())
    ax2[2].set_ylabel('Acceleration (g)', color='r')

    axs[1,1].set_xlabel('time (s)')
    axs[1,1].set_title('Model Inputs: Steering Wheel Angle (deg), Input Throttle (%)', color='k')
    axs[1,1].tick_params(axis='y', labelcolor='k')
    axs[1,1].plot(df_in.t, df_in.sw_angle, color='k')
    axs[1,1].plot(df_in.t, df_in.throttle, color='r')
    axs[1,1].set_ylabel('Velocity (mph) | Steering Angle (deg)', color='k')

    ax2.append(axs[1,1].twinx())
    ax2[3].plot(df_in.t, df_in.brake, color='b')
    ax2[3].tick_params(axis='y', labelcolor='b')
    ax2[3].set_ylabel('Input Brake', color='b')

    plt.subplots_adjust(wspace=.6, hspace = .6)
    plt.show()

def plot_vehicle_pre_motion(df_in, pre_df):
    pre_df['V'] = np.sqrt(pre_df.Vx**2 + pre_df.Vy**2)/ 1.46667 
    fig, axs = plt.subplots(3, 2, figsize=(18,8), sharex='col')
    axs[0,0].set_xlabel('Time (s)')
    axs[0,0].set_ylabel('Velocity (mph) (Vx, Vy)', color='k')
    axs[0,0].plot(df_in.t - df_in.t[0], df_in.v_edr / 1.46667, color='k', linestyle='dashed', label = 'V - EDR')
    axs[0,0].plot(pre_df.t, pre_df.Vx / 1.46667, color='k', label = 'Vx')    
    axs[0,0].plot(pre_df.t, pre_df.Vy / 1.46667, color='b', label = 'Vy')
    axs[0,0].plot(pre_df.t, pre_df.V, color = 'g', linestyle='dashed', label = 'V')
    axs[0,0].tick_params(axis='y', labelcolor='k')
    axs[0,0].legend(frameon = False)

    #axs[0,1].set_xlabel('Time (s)')
    axs[0,1].set_ylabel('Acceleration (g)', color='k')
    axs[0,1].tick_params(axis='y', labelcolor='k')
    axs[0,1].plot(pre_df.t, pre_df.Ax/32.2, color='k', label = 'Ax')
    axs[0,1].plot(pre_df.t, pre_df.Ay/32.2, color='b', label = 'Ay')
    axs[0,1].plot(pre_df.t, pre_df.ax/32.2, color='k', linestyle='dashed', label = 'ax')
    axs[0,1].plot(pre_df.t, pre_df.ay/32.2, color='b', linestyle='dashed', label = 'ay')
    axs[0,1].legend(frameon = False)

    #axs[1,0].set_xlabel('Time (s)')
    axs[1,0].set_ylabel('Forward Tire Forces (lb)', color='k')
    axs[1,0].tick_params(axis='y', labelcolor='k')
    axs[1,0].plot(pre_df.t, pre_df.lf_fx, color='b')
    axs[1,0].plot(pre_df.t, pre_df.rf_fx, color='g')
    axs[1,0].plot(pre_df.t, pre_df.rr_fx, color='m')
    axs[1,0].plot(pre_df.t, pre_df.lr_fx, color='orange')

    #axs[1,1].set_xlabel('Time (s)')
    axs[1,1].set_ylabel('Rightward Tire Forces (lb)', color='k')
    axs[1,1].tick_params(axis='y', labelcolor='k')
    axs[1,1].plot(pre_df.t, pre_df.lf_fy, color='b')
    axs[1,1].plot(pre_df.t, pre_df.rf_fy, color='g')
    axs[1,1].plot(pre_df.t, pre_df.rr_fy, color='m')
    axs[1,1].plot(pre_df.t, pre_df.lr_fy, color='orange')

    axs[2,0].set_xlabel('Time (s)')
    axs[2,0].set_ylabel('Omega (deg/s), Alpha (deg/s/s)', color='k')
    axs[2,0].tick_params(axis='y', labelcolor='k')
    axs[2,0].plot(pre_df.t, pre_df.oz_deg, color='k')
    axs[2,0].plot(pre_df.t, pre_df.alphaz_deg, color='r')
    axs[2,0].plot(df_in.t - df_in.t[0], df_in.oz_edr, color='k', linestyle='dashed')

    axs[2,1].set_xlabel('Time (s)')
    axs[2,1].set_ylabel('Heading Angle (deg)', color='k')
    axs[2,1].tick_params(axis='y', labelcolor='k')
    axs[2,1].plot(pre_df.t, pre_df.theta_deg, color='k')

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

    plt.subplots_adjust(wspace=0.2, hspace = .1)
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
    plt.scatter(draw_vx.lrw[i], draw_vy.lrw[i], c='orange')       # left rear wheel center
    plt.plot(lrw_x, lrw_y, 'orange')

    # vehicle CG
    plt.scatter(draw_vx.cg[i], draw_vy.cg[i],s=500, c='k')

    # velocity vector

    plt.arrow(draw_vx.cg[i], draw_vy.cg[i], draw_vx.vel_v[i]-draw_vx.cg[i], draw_vy.vel_v[i]-draw_vy.cg[i], head_width=.5, head_length=0.5, fc='r', ec='r')

    # vehicle axes
    plt.arrow(draw_vx.cg[i], draw_vy.cg[i], draw_vx.xaxis[i]-draw_vx.cg[i], draw_vy.xaxis[i]-draw_vy.cg[i], head_width=.5, head_length=0.5, fc='k', ec='k')
    plt.arrow(draw_vx.cg[i], draw_vy.cg[i], draw_vx.yaxis[i]-draw_vx.cg[i], draw_vy.yaxis[i]-draw_vy.cg[i], head_width=.5, head_length=0.5, fc='b', ec='b')
    plt.gca().invert_yaxis()
    plt.show()

def draw_vehicle_motion(draw_gx, draw_gy, draw_tire, i):
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


    fig = plt.figure(figsize=(15,10))
    #plt.xlim([-300, 50])
    #plt.ylim([-100, 100])

    plt.plot(bdy_x, bdy_y, 'k')
    plt.scatter(draw_gx.lfw[i], draw_gy.lfw[i], c='b')       # left front wheel center
    plt.plot(lfw_x, lfw_y, 'b')
    plt.scatter(draw_gx.rfw[i], draw_gy.rfw[i], c='g')       # right front wheel center
    plt.plot(rfw_x, rfw_y, 'g')
    plt.scatter(draw_gx.rrw[i], draw_gy.rrw[i], c='m')       # right rear wheel center
    plt.plot(rrw_x, rrw_y,'m')
    plt.scatter(draw_gx.lrw[i], draw_gy.lrw[i], c='orange')       # left rear wheel center
    plt.plot(lrw_x, lrw_y, 'orange')
    plt.scatter(draw_gx.cg[i], draw_gy.cg[i],s=100, c='k')                                # vehicle CG
    plt.arrow(draw_gx.cg[i], draw_gy.cg[i], draw_gx.vel_v[i]*0.2, draw_gy.vel_v[i]*0.2, head_width=.5, head_length=0.5, fc='r', ec='r')     # velocity vector
    plt.arrow(draw_gx.cg[i], draw_gy.cg[i], draw_gx.xaxis[i]-draw_gx.cg[i], draw_gy.xaxis[i]-draw_gy.cg[i], head_width=.5, head_length=0.5, fc='k', ec='k')     # vehicle axes
    plt.arrow(draw_gx.cg[i], draw_gy.cg[i], draw_gx.yaxis[i]-draw_gx.cg[i], draw_gy.yaxis[i]-draw_gy.cg[i], head_width=.5, head_length=0.5, fc='b', ec='b')     # vehicle axes

    # for loop up to i
    if draw_tire == 1:
        for i in range(0, i):
            if draw_gx.loc[i, 'lf_lock'] == 0:
                plt.scatter(draw_gx.loc[i, 'lfw'], draw_gy.loc[i, 'lfw'], c = 'b', s = 1, marker = '.')
            elif draw_gx.loc[i, 'lf_lock'] == 1:
                plt.scatter(draw_gx.loc[i, 'lfw'], draw_gy.loc[i, 'lfw'], c = 'b', s = 4, marker = 's')

            if draw_gx.loc[i, 'rf_lock'] == 0:
                plt.scatter(draw_gx.loc[i, 'rfw'], draw_gy.loc[i, 'rfw'], c = 'g', s = 1, marker = '.')
            elif draw_gx.loc[i, 'rf_lock'] == 1:
                plt.scatter(draw_gx.loc[i, 'rfw'], draw_gy.loc[i, 'rfw'], c = 'g', s = 4, marker = 's')

            if draw_gx.loc[i, 'rr_lock'] == 0:
                plt.scatter(draw_gx.loc[i, 'rrw'], draw_gy.loc[i, 'rrw'], c = 'm', s = 1, marker = '.')
            elif draw_gx.loc[i, 'rr_lock'] == 1:
                plt.scatter(draw_gx.loc[i, 'rrw'], draw_gy.loc[i, 'rrw'], c = 'm', s = 4, marker = 's')

            if draw_gx.loc[i, 'lr_lock'] == 0:
                plt.scatter(draw_gx.loc[i, 'lrw'], draw_gy.loc[i, 'lrw'], c = 'orange', s = 1, marker = '.')
            elif draw_gx.loc[i, 'lr_lock'] == 1:
                plt.scatter(draw_gx.loc[i, 'lrw'], draw_gy.loc[i, 'lrw'], c = 'orange', s = 4, marker = 's')

    plt.gca().invert_yaxis()
    plt.show()
    return fig

def draw_vehicle_motion_loop(draw_gx, draw_gy, draw_tire, ax, i):
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


  
    #plt.xlim([-300, 50])
    #plt.ylim([-100, 100])

    ax.plot(bdy_x, bdy_y, 'k')
    ax.scatter(draw_gx.lfw[i], draw_gy.lfw[i], c='b')       # left front wheel center
    ax.plot(lfw_x, lfw_y, 'b')
    ax.scatter(draw_gx.rfw[i], draw_gy.rfw[i], c='g')       # right front wheel center
    ax.plot(rfw_x, rfw_y, 'g')
    ax.scatter(draw_gx.rrw[i], draw_gy.rrw[i], c='m')       # right rear wheel center
    ax.plot(rrw_x, rrw_y,'m')
    ax.scatter(draw_gx.lrw[i], draw_gy.lrw[i], c='orange')       # left rear wheel center
    ax.plot(lrw_x, lrw_y, 'orange')
    ax.scatter(draw_gx.cg[i], draw_gy.cg[i],s=100, c='k')                                # vehicle CG
    ax.arrow(draw_gx.cg[i], draw_gy.cg[i], draw_gx.vel_v[i]*0.2, draw_gy.vel_v[i]*0.2, head_width=.5, head_length=0.5, fc='r', ec='r')     # velocity vector
    ax.arrow(draw_gx.cg[i], draw_gy.cg[i], draw_gx.xaxis[i]-draw_gx.cg[i], draw_gy.xaxis[i]-draw_gy.cg[i], head_width=.5, head_length=0.5, fc='k', ec='k')     # vehicle axes
    ax.arrow(draw_gx.cg[i], draw_gy.cg[i], draw_gx.yaxis[i]-draw_gx.cg[i], draw_gy.yaxis[i]-draw_gy.cg[i], head_width=.5, head_length=0.5, fc='b', ec='b')     # vehicle axes

    # for loop up to i
    if draw_tire == 1:
        for i in range(0, i):
            if draw_gx.loc[i, 'lf_lock'] == 0:
                ax.scatter(draw_gx.loc[i, 'lfw'], draw_gy.loc[i, 'lfw'], c = 'b', s = 1, marker = '.')
            elif draw_gx.loc[i, 'lf_lock'] == 1:
                ax.scatter(draw_gx.loc[i, 'lfw'], draw_gy.loc[i, 'lfw'], c = 'b', s = 4, marker = 's')

            if draw_gx.loc[i, 'rf_lock'] == 0:
                ax.scatter(draw_gx.loc[i, 'rfw'], draw_gy.loc[i, 'rfw'], c = 'g', s = 1, marker = '.')
            elif draw_gx.loc[i, 'rf_lock'] == 1:
                ax.scatter(draw_gx.loc[i, 'rfw'], draw_gy.loc[i, 'rfw'], c = 'g', s = 4, marker = 's')

            if draw_gx.loc[i, 'rr_lock'] == 0:
                ax.scatter(draw_gx.loc[i, 'rrw'], draw_gy.loc[i, 'rrw'], c = 'm', s = 1, marker = '.')
            elif draw_gx.loc[i, 'rr_lock'] == 1:
                ax.scatter(draw_gx.loc[i, 'rrw'], draw_gy.loc[i, 'rrw'], c = 'm', s = 4, marker = 's')

            if draw_gx.loc[i, 'lr_lock'] == 0:
                ax.scatter(draw_gx.loc[i, 'lrw'], draw_gy.loc[i, 'lrw'], c = 'orange', s = 1, marker = '.')
            elif draw_gx.loc[i, 'lr_lock'] == 1:
                ax.scatter(draw_gx.loc[i, 'lrw'], draw_gy.loc[i, 'lrw'], c = 'orange', s = 4, marker = 's')

    plt.gca().invert_yaxis()
    #plt.show()
    return

def draw_vehicle_motion_outline(draw_gx, draw_gy, draw_tire, i):
    #%% Plot Vehicle in Global reference frame

    bdy_x = (draw_gx.b_lfc[i], draw_gx.b_rfc[i], draw_gx.b_rrc[i], draw_gx.b_lrc[i], draw_gx.b_lfc[i])
    bdy_y = (draw_gy.b_lfc[i], draw_gy.b_rfc[i], draw_gy.b_rrc[i], draw_gy.b_lrc[i], draw_gy.b_lfc[i])

    fig = plt.figure(figsize=(15,10))
    plt.xlim([-10, 1000])
    plt.ylim([-300, 300])

    plt.plot(bdy_x, bdy_y, 'k')
    plt.scatter(draw_gx.lfw[i], draw_gy.lfw[i], c='b')       # left front wheel center
    plt.scatter(draw_gx.rfw[i], draw_gy.rfw[i], c='g')       # right front wheel center
    plt.scatter(draw_gx.rrw[i], draw_gy.rrw[i], c='m')       # right rear wheel center
    plt.scatter(draw_gx.lrw[i], draw_gy.lrw[i], c='orange')       # left rear wheel center
    plt.scatter(draw_gx.cg[i], draw_gy.cg[i],s=100, c='k')                                # vehicle CG
    plt.arrow(draw_gx.cg[i], draw_gy.cg[i], draw_gx.vel_v[i], draw_gy.vel_v[i], head_width=.5, head_length=0.5, fc='r', ec='r')     # velocity vector
    plt.arrow(draw_gx.cg[i], draw_gy.cg[i], draw_gx.xaxis[i]-draw_gx.cg[i], draw_gy.xaxis[i]-draw_gy.cg[i], head_width=.5, head_length=0.5, fc='k', ec='k')     # vehicle axes
    plt.arrow(draw_gx.cg[i], draw_gy.cg[i], draw_gx.yaxis[i]-draw_gx.cg[i], draw_gy.yaxis[i]-draw_gy.cg[i], head_width=.5, head_length=0.5, fc='b', ec='b')     # vehicle axes

    # for loop up to i
    if draw_tire == 1:
        for i in range(0, i):
            if draw_gx.loc[i, 'lf_lock'] == 0:
                plt.scatter(draw_gx.loc[i, 'lfw'], draw_gy.loc[i, 'lfw'], c = 'b', s = 1, marker = '.')
            elif draw_gx.loc[i, 'lf_lock'] == 1:
                plt.scatter(draw_gx.loc[i, 'lfw'], draw_gy.loc[i, 'lfw'], c = 'b', s = 4, marker = 's')

            if draw_gx.loc[i, 'rf_lock'] == 0:
                plt.scatter(draw_gx.loc[i, 'rfw'], draw_gy.loc[i, 'rfw'], c = 'g', s = 1, marker = '.')
            elif draw_gx.loc[i, 'rf_lock'] == 1:
                plt.scatter(draw_gx.loc[i, 'rfw'], draw_gy.loc[i, 'rfw'], c = 'g', s = 4, marker = 's')

            if draw_gx.loc[i, 'rr_lock'] == 0:
                plt.scatter(draw_gx.loc[i, 'rrw'], draw_gy.loc[i, 'rrw'], c = 'm', s = 1, marker = '.')
            elif draw_gx.loc[i, 'rr_lock'] == 1:
                plt.scatter(draw_gx.loc[i, 'rrw'], draw_gy.loc[i, 'rrw'], c = 'm', s = 4, marker = 's')

            if draw_gx.loc[i, 'lr_lock'] == 0:
                plt.scatter(draw_gx.loc[i, 'lrw'], draw_gy.loc[i, 'lrw'], c = 'orange', s = 1, marker = '.')
            elif draw_gx.loc[i, 'lr_lock'] == 1:
                plt.scatter(draw_gx.loc[i, 'lrw'], draw_gy.loc[i, 'lrw'], c = 'orange', s = 4, marker = 's')

    plt.gca().invert_yaxis()
    plt.show()
    return fig


def draw_vehicles_impact(draw_gx1, draw_gy1, draw_gx2, draw_gy2, thetac):
    draw_gx = draw_gx1.append(draw_gx2, ignore_index = True)
    draw_gy = draw_gy1.append(draw_gy2, ignore_index = True)

    dx_t = 20 * math.cos(thetac)
    dy_t = 20 * math.sin(thetac)
    dx_n = 10 * math.cos(thetac+90*math.pi/180)
    dy_n = 10 * math.sin(thetac+90*math.pi/180)

    fig = plt.figure(figsize=(15,10))

    for i in (range(len(draw_gx))):
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


        plt.plot(bdy_x, bdy_y, 'k')
        plt.scatter(draw_gx.lfw[i], draw_gy.lfw[i], c='b')       # left front wheel center
        plt.plot(lfw_x, lfw_y, 'b')
        plt.scatter(draw_gx.rfw[i], draw_gy.rfw[i], c='g')       # right front wheel center
        plt.plot(rfw_x, rfw_y, 'g')
        plt.scatter(draw_gx.rrw[i], draw_gy.rrw[i], c='m')       # right rear wheel center
        plt.plot(rrw_x, rrw_y,'m')
        plt.scatter(draw_gx.lrw[i], draw_gy.lrw[i], c='orange')       # left rear wheel center
        plt.plot(lrw_x, lrw_y, 'orange')

        if i == 0:
            plt.scatter(draw_gx.cg[i], draw_gy.cg[i],s=100, c='b')                                  # vehicle 1 CG
        if i == 1:
            plt.scatter(draw_gx.cg[i], draw_gy.cg[i],s=100, c='g')                                  # vehicle 2 CG

        plt.scatter(draw_gx.poi[i], draw_gy.poi[i],s=100, c='r')                                # POI
        plt.arrow(draw_gx.cg[i], draw_gy.cg[i], draw_gx.vel_v[i]-draw_gx.cg[i], draw_gy.vel_v[i]-draw_gy.cg[i], head_width=.5, head_length=0.5, fc='r', ec='r')     # velocity vector
        plt.arrow(draw_gx.cg[i], draw_gy.cg[i], draw_gx.xaxis[i]-draw_gx.cg[i], draw_gy.xaxis[i]-draw_gy.cg[i], head_width=.5, head_length=0.5, fc='k', ec='k')     # vehicle axes
        plt.arrow(draw_gx.cg[i], draw_gy.cg[i], draw_gx.yaxis[i]-draw_gx.cg[i], draw_gy.yaxis[i]-draw_gy.cg[i], head_width=.5, head_length=0.5, fc='b', ec='b')     # vehicle axes

    plt.arrow(draw_gx.poi[i], draw_gy.poi[i], dx_t, dy_t, head_width=.8, head_length=0.8, fc='k', ec='r', linestyle = '--')     # collision plane - tangent
    plt.arrow(draw_gx.poi[i], draw_gy.poi[i], dx_n, dy_n, head_width=.8, head_length=0.8, fc='r', ec='r', linestyle = '--')     # collision plane - normal
    plt.xlim([-50, 50])
    plt.ylim([-30, 30])
    plt.gca().invert_yaxis()
    plt.show()
    return fig

def draw_impact_motion(draw_gx1, draw_gy1, draw_gx2, draw_gy2, draw_tire, i):

    #%% Plot Vehicle in Global reference frame
    fig = plt.figure(figsize=(15,10))

    for j in range(0,2):
        if j == 0:
            draw_gx = draw_gx1
            draw_gy = draw_gy1
        elif j == 1:
            draw_gx = draw_gx2
            draw_gy = draw_gy2

        for i in [0,i]:
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

            plt.plot(bdy_x, bdy_y, 'k')
            plt.scatter(draw_gx.lfw[i], draw_gy.lfw[i], c='b')       # left front wheel center
            plt.plot(lfw_x, lfw_y, 'b')
            plt.scatter(draw_gx.rfw[i], draw_gy.rfw[i], c='g')       # right front wheel center
            plt.plot(rfw_x, rfw_y, 'g')
            plt.scatter(draw_gx.rrw[i], draw_gy.rrw[i], c='m')       # right rear wheel center
            plt.plot(rrw_x, rrw_y,'m')
            plt.scatter(draw_gx.lrw[i], draw_gy.lrw[i], c='orange')       # left rear wheel center
            plt.plot(lrw_x, lrw_y, 'orange')
            plt.scatter(draw_gx.cg[i], draw_gy.cg[i],s=100, c='k')                                # vehicle CG
            plt.arrow(draw_gx.cg[i], draw_gy.cg[i], draw_gx.vel_v[i]-draw_gx.cg[i], draw_gy.vel_v[i]-draw_gy.cg[i], head_width=.5, head_length=0.5, fc='r', ec='r')     # velocity vector
            plt.arrow(draw_gx.cg[i], draw_gy.cg[i], draw_gx.xaxis[i]-draw_gx.cg[i], draw_gy.xaxis[i]-draw_gy.cg[i], head_width=.5, head_length=0.5, fc='k', ec='k')     # vehicle axes
            plt.arrow(draw_gx.cg[i], draw_gy.cg[i], draw_gx.yaxis[i]-draw_gx.cg[i], draw_gy.yaxis[i]-draw_gy.cg[i], head_width=.5, head_length=0.5, fc='b', ec='b')     # vehicle axes

        # for loop up to i
        if draw_tire == 1:
            for i in range(0, i):
                if draw_gx.loc[i, 'lf_lock'] == 0:
                    plt.scatter(draw_gx.loc[i, 'lfw'], draw_gy.loc[i, 'lfw'], c = 'b', s = 1, marker = '.')
                elif draw_gx.loc[i, 'lf_lock'] == 1:
                    plt.scatter(draw_gx.loc[i, 'lfw'], draw_gy.loc[i, 'lfw'], c = 'b', s = 4, marker = 's')

                if draw_gx.loc[i, 'rf_lock'] == 0:
                    plt.scatter(draw_gx.loc[i, 'rfw'], draw_gy.loc[i, 'rfw'], c = 'g', s = 1, marker = '.')
                elif draw_gx.loc[i, 'rf_lock'] == 1:
                    plt.scatter(draw_gx.loc[i, 'rfw'], draw_gy.loc[i, 'rfw'], c = 'g', s = 4, marker = 's')

                if draw_gx.loc[i, 'rr_lock'] == 0:
                    plt.scatter(draw_gx.loc[i, 'rrw'], draw_gy.loc[i, 'rrw'], c = 'm', s = 1, marker = '.')
                elif draw_gx.loc[i, 'rr_lock'] == 1:
                    plt.scatter(draw_gx.loc[i, 'rrw'], draw_gy.loc[i, 'rrw'], c = 'm', s = 4, marker = 's')

                if draw_gx.loc[i, 'lr_lock'] == 0:
                    plt.scatter(draw_gx.loc[i, 'lrw'], draw_gy.loc[i, 'lrw'], c = 'orange', s = 1, marker = '.')
                elif draw_gx.loc[i, 'lr_lock'] == 1:
                    plt.scatter(draw_gx.loc[i, 'lrw'], draw_gy.loc[i, 'lrw'], c = 'orange', s = 4, marker = 's')


    plt.xlim([-300, 50])
    plt.ylim([-100, 100])
    plt.gca().invert_yaxis()
    plt.show()
    return fig
