"""
seperate function for SDOF models / sideswipe / impulse momentum
- SDOF = single vector for PDOF
- sideswipe - single point
- IPCM - normal / tangent vectors


user inputs are used to generate an impact point and directions for tangent and normal plane

needs vehicle geometry

# prescribed points, P1, P2, P3, P4 will automatically select right front, right rear, left rear or left front corner

inputs, as dictionary? -
static inputs:
impact_point = (x, y) or P1, P2, P3, P4
normal_angle = angle (deg) - direction of normal impact plane in vehicle coordinates

dynamic inputs: vehicle 1 cg(x, y, theta)

in SDOF models, normal angle indicates the PDOF and forces are applied in that direction only

tracks impact point on provides global coorindate and orientation
will be used to detect impact with edge on vehicle 2



"""

import pandas as pd
import numpy as np

# TODO: create input for figure size - loads from "defaults" folder?
figure_size = (16,9)

def impact_edge(self):
    """
    generates an edge in vehicle 2 (struck) reference frame
    sideswipe collisions - edge will determine the extent of vehcle engagement with respect
    to contacting point in vehicle 1 (striking)
    impact momentum model - impact edge will be used along with the impact plane to determine time
    of impact
    """
    # test for required inputs
    if not self.lcgf:
        self.lcgf = float(input("Enter CG to front axle (ft)"))
    
    if not self.lcgr:
        self.lcgr = float(input("Enter CG to rear axle (ft)"))

    if not self.f_hang:
        self.f_hang = float(input("Enter front overhang (ft)"))

    if not self.r_hang:
        self.r_hang = float(input("Enter rear overhang (ft)"))

    if not self.v_width:
        self.v_width = float(input("Enter vehicle width (ft)"))

    # create figure of vehicle 1 with scale / grid and p1, p2, p3, p4 labeled when function is called
    # option 5 = custom location
    
    # x,y coordinates of vehicle outline:
    # left front corner
    self._b_lfc_x = self.lcgf + self.f_hang  
    self._b_lfc_y = -1 * self.v_width / 2
    # right front corner
    self._b_rfc_x = self.lcgf + self.f_hang
    self._b_rfc_y = self.v_width / 2
    # right rear corner
    self._b_rrc_x = -1 * self.lcgr - self.r_hang
    self._b_rrc_y = self.v_width / 2
    # left rear corner
    self._b_lrc_x = -1 * self.lcgr - self.r_hang
    self._b_lrc_y = -1* self.v_width / 2

    bdy_x = (self._b_lfc_x, self._b_rfc_x, self._b_rrc_x, self._b_lrc_x, self._b_lfc_x)
    bdy_y = (self._b_lfc_y, self._b_rfc_y, self._b_rrc_y, self._b_lrc_y, self._b_lfc_y)

    # generate plot to show vehicle outline and default points for impact
    plt.figure(figsize=figure_size)
    plt.xlim([self._b_lrc_x * 1.5, self._b_lfc_x * 1.5])

    # adjust y axis length to keep aspect ratio defined in figure size
    x_axis_length = self._b_lfc_x * 1.5 - self._b_lrc_x * 1.5
    plt.ylim([-0.5 * x_axis_length * figure_size[1] / figure_size[0],
              0.5 * x_axis_length * figure_size[1] / figure_size[0]])
    
    plt.plot(bdy_x[:2], bdy_y[:2], 'k')
    plt.plot(bdy_x[1:3], bdy_y[1:3], 'b')
    plt.plot(bdy_x[2:4], bdy_y[2:4], 'g')
    plt.plot(bdy_x[3:5], bdy_y[3:5], 'orange')

    plt.text(self._b_lfc_x, 0, "1", horizontalalignment = 'right')
    plt.text(0, -1.1 * self.v_width / 2, "2", horizontalalignment = 'center')
    plt.text(self._b_rrc_x * 1.1, 0, "3", horizontalalignment = 'left')
    plt.text(0, 1.1 * self.v_width / 2, "4", horizontalalignment = 'center')
    plt.gca().invert_yaxis()
    plt.show(block=False)


    impact_option = int(input("Choose option for impact edge"))

    if impact_option not in [1, 2, 3, 4]:
        raise ValueError("Invalid impact edge option - enter 1, 2, 3, 4)
    else:
        if impact_option == 1:
            self.edgeimpact_x1 = self.lcgf + self.f_hang
            self.edgeimpact_y1 = -1 * self.v_width / 2
            self.edgeimpact_x2 = self.lcgf + self.f_hang
            self.edgeimpact_y2 = self.v_width / 2 
        elif impact_option == 2:
            self.edgeimpact_x1 = self.lcgf + self.f_hang
            self.edgeimpact_y1 = self.v_width / 2
            self.edgeimpact_x2 = -1 * self.lcgr - self.r_hang
            self.edgeimpact_y2 = self.v_width / 2
        elif impact_option == 3:
            self.edgeimpact_x1 = -1 * self.lcgr - self.r_hang
            self.edgeimpact_y1 = self.v_width / 2
            self.edgeimpact_x2 = -1 * self.lcgr - self.r_hang
            self.edgeimpact_y2 = -1* self.v_width / 2
        elif impact_option == 4:
            self.edgeimpact_x1 = -1 * self.lcgr - self.r_hang
            self.edgeimpact_y1 = -1 * self.v_width / 2
            self.edgeimpact_x2 = self.lcgf + self.f_hang
            self.edgeimpact_y2 = -1 * self.v_width / 2


    # draw vehicle with impact edge location


# create plot of vehicle 1 so that impact point can be chosen

v_info = pd.read_excel('Input.xlsx', sheet_name = 'vehicles', header = 0)

# X,Y dataframes for drawing vehicle
# hard code these columns:
head = pd.read_excel('Input.xlsx',sheet_name = 'draw_columns')
columns = head.columns.values.tolist() # Column Headers
columns = [xx,xx,xx,xx]
# create nested dict based on initial inputs for both vehicles
VehicleData = {v1, v2}

DrawVehicleX = pd.DataFrame(columns = columns)                                      # time variant vehicle geometry for plotting in vehicle frame
DrawVehicleY = pd.DataFrame(columns = columns)                                      # time variant vehicle geometry for plotting in vehicle frame


# coordinates for vehicle body and wheels
DrawVehicleX = DrawVehicleX.append({'b_lfc': v_dict['lcgf'] + v_dict['f_hang'],     # body outline
                          'b_rfc': v_dict['lcgf'] + v_dict['f_hang'],
                          'b_rrc': -1* (v_dict['lcgr'] + v_dict['r_hang']),
                          'b_lrc': -1* (v_dict['lcgr'] + v_dict['r_hang']),
                          'lfw': v_dict['lcgf'],                         # left front wheel + initial turn
                          'lfw_a': v_dict['lcgf'] + v_dict['tire_d']/2*math.cos(vin.loc[i,'delta_rad']) - -1*v_dict['tire_w']/2*math.sin(vin.loc[i,'delta_rad']),
                          'lfw_b': v_dict['lcgf'] + v_dict['tire_d']/2*math.cos(vin.loc[i,'delta_rad']) - v_dict['tire_w']/2*math.sin(vin.loc[i,'delta_rad']),
                          'lfw_c': v_dict['lcgf'] + -1*v_dict['tire_d']/2*math.cos(vin.loc[i,'delta_rad']) - v_dict['tire_w']/2*math.sin(vin.loc[i,'delta_rad']),
                          'lfw_d': v_dict['lcgf'] + -1*v_dict['tire_d']/2*math.cos(vin.loc[i,'delta_rad']) - -1*v_dict['tire_w']/2*math.sin(vin.loc[i,'delta_rad']),
                          'rfw': v_dict['lcgf'],                         # Right front wheel + initial turn
                          'rfw_a': v_dict['lcgf'] + v_dict['tire_d']/2*math.cos(vin.loc[i,'delta_rad']) - -1*v_dict['tire_w']/2*math.sin(vin.loc[i,'delta_rad']),
                          'rfw_b': v_dict['lcgf'] + v_dict['tire_d']/2*math.cos(vin.loc[i,'delta_rad']) - v_dict['tire_w']/2*math.sin(vin.loc[i,'delta_rad']),
                          'rfw_c': v_dict['lcgf'] + -1*v_dict['tire_d']/2*math.cos(vin.loc[i,'delta_rad']) - v_dict['tire_w']/2*math.sin(vin.loc[i,'delta_rad']),
                          'rfw_d': v_dict['lcgf'] + -1*v_dict['tire_d']/2*math.cos(vin.loc[i,'delta_rad']) - -1*v_dict['tire_w']/2*math.sin(vin.loc[i,'delta_rad']),
                          'rrw': -1*v_dict['lcgr'],                          # Right rear wheel
                          'rrw_a': -1*v_dict['lcgr'] + v_dict['tire_d']/2,
                          'rrw_b': -1*v_dict['lcgr'] + v_dict['tire_d']/2,
                          'rrw_c': -1*v_dict['lcgr'] - v_dict['tire_d']/2,
                          'rrw_d': -1*v_dict['lcgr'] - v_dict['tire_d']/2,
                          'lrw': -1*v_dict['lcgr'],                          # Left rear wheel
                          'lrw_a': -1*v_dict['lcgr'] + v_dict['tire_d']/2,
                          'lrw_b': -1*v_dict['lcgr'] + v_dict['tire_d']/2,
                          'lrw_c': -1*v_dict['lcgr'] - v_dict['tire_d']/2,
                          'lrw_d': -1*v_dict['lcgr'] - v_dict['tire_d']/2,
                          'cg': 0,                                         # CG
                          'xaxis':v_dict['lcgf'] + v_dict['f_hang']+1.5,   # line for x-axis
                          'yaxis': 0,                                      # line for y-axis
                          'vel_v':10*math.cos(vin.beta_rad[i])}, ignore_index=True)  # line for initial velocity vector

DrawVehicleY = DrawVehicleY.append({'b_lfc': -1*v_dict['v_width']/2,     # body outline
                          'b_rfc': v_dict['v_width']/2,
                          'b_rrc': v_dict['v_width']/2,
                          'b_lrc': -1*v_dict['v_width']/2,
                          'lfw':  -1 * (v_dict['v_width']/2 - v_dict['tire_w']/2),                         # left front wheel + initial turn
                          'lfw_a': -1 * (v_dict['v_width']/2 - v_dict['tire_w']/2) + v_dict['tire_d']/2*math.sin(vin.loc[i,'delta_rad']) + -1*v_dict['tire_w']/2*math.cos(vin.loc[i,'delta_rad']),
                          'lfw_b': -1 * (v_dict['v_width']/2 - v_dict['tire_w']/2) + v_dict['tire_d']/2*math.sin(vin.loc[i,'delta_rad']) + v_dict['tire_w']/2*math.cos(vin.loc[i,'delta_rad']),
                          'lfw_c': -1 * (v_dict['v_width']/2 - v_dict['tire_w']/2) + -1*v_dict['tire_d']/2*math.sin(vin.loc[i,'delta_rad']) + v_dict['tire_w']/2*math.cos(vin.loc[i,'delta_rad']),
                          'lfw_d': -1 * (v_dict['v_width']/2 - v_dict['tire_w']/2) + -1*v_dict['tire_d']/2*math.sin(vin.loc[i,'delta_rad']) + -1*v_dict['tire_w']/2*math.cos(vin.loc[i,'delta_rad']),
                          'rfw': (v_dict['v_width']/2 - v_dict['tire_w']/2),                         # Right front wheel + initial turn
                          'rfw_a': (v_dict['v_width']/2 - v_dict['tire_w']/2) + v_dict['tire_d']/2*math.sin(vin.loc[i,'delta_rad']) + -1*v_dict['tire_w']/2*math.cos(vin.loc[i,'delta_rad']),
                          'rfw_b':(v_dict['v_width']/2 - v_dict['tire_w']/2) + v_dict['tire_d']/2*math.sin(vin.loc[i,'delta_rad']) + v_dict['tire_w']/2*math.cos(vin.loc[i,'delta_rad']),
                          'rfw_c':(v_dict['v_width']/2 - v_dict['tire_w']/2) + -1*v_dict['tire_d']/2*math.sin(vin.loc[i,'delta_rad']) + v_dict['tire_w']/2*math.cos(vin.loc[i,'delta_rad']),
                          'rfw_d':(v_dict['v_width']/2 - v_dict['tire_w']/2) + -1*v_dict['tire_d']/2*math.sin(vin.loc[i,'delta_rad']) + -1*v_dict['tire_w']/2*math.cos(vin.loc[i,'delta_rad']),
                          'rrw': (v_dict['v_width']/2 - v_dict['tire_w']/2),                          # Right rear wheel
                          'rrw_a':v_dict['v_width']/2 - v_dict['tire_w'],
                          'rrw_b': v_dict['v_width']/2,
                          'rrw_c':v_dict['v_width']/2,
                          'rrw_d':v_dict['v_width']/2 - v_dict['tire_w'],
                          'lrw': -1 * (v_dict['v_width']/2 - v_dict['tire_w']/2),                          # Left rear wheel
                          'lrw_a': -1 * v_dict['v_width']/2,
                          'lrw_b': -1 * v_dict['v_width']/2 + v_dict['tire_w'],
                          'lrw_c': -1 * v_dict['v_width']/2 + v_dict['tire_w'],
                          'lrw_d': -1 * v_dict['v_width']/2,
                          'cg': 0,                                         # CG
                          'xaxis':0,   # line for x-axis
                          'yaxis': v_dict['v_width']/2+1.5,                                      # line for y-axis
                          'vel_v':10*math.sin(vin.beta_rad[i])}, ignore_index=True)  # line for initial velocity vector
