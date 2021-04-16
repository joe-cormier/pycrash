
import pandas as pd
import numpy as np
import csv
import os
dt_impact = 0.001
mu_max = 0.9

"""
Performs interative calculations for the SDOF impact simulation
"""
# TODO: update to take user defined inputs

# Functions
# v2 brake force wil oppose the spring force as long as the vehicle is moving forward
def BrakeCheck(brake_applied, springF, v):
    if v > 0:                 # vehicle is in motion - full brake force applied
        return brake_applied * -1 * sign(v)
    if brake_applied == 0:    # no brake applied - brake force will be zero
        return 0
    elif abs(springF) > brake_applied: # spring force is greater than brake force full brake force applied
        return brake_applied * -1
    elif abs(springF) < brake_applied: # spring force is less than braking force so accel will = 0
            return springF * -1

def sign(x):
    # returns the sign of a number
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return x

def SingleDOFmodel(W1, v1_initial, v1_brake, W2, v2_initial, v2_brake, k, cor,
                    tstop, ktype, ttype):

    _tstop = 0 # default limit for ttype == 0 will use tstop otherwise

    if (ttype == 0):
        tstop = _tstop

    # import correct spring force model based on model type
    if (ktype == 'constantK'):
        from .spring_models import SpringForce as SpringForce  # TODO: fix import name
        input_k_disp = 0                # unused input so same function can be used for both conditions
        input_k_force = 0
    elif (ktype == 'tableK'):
        from .spring_models import SpringFdx as SpringForce
        # inputs for model
        input_k_disp = k.iloc[:, 0]
        input_k_force = k.iloc[:, 1]
        k = 0                           # unused input for table based stiffness
    else:
        print("Unknown Model Type")

    # initialize data columns
    columns = ['t', 'x1', 'x2', 'v1', 'v2', 'a1', 'a2', 'springF', 'dx', 'v1_brakeF', 'v2_brakeF']
    spring_model = pd.DataFrame(columns=columns)

    ##################################### SDOF Model ############################################
    # model will produce increasing mutual crush until a common velocity is reached, then mutual crush will decrease
    # model will then use COR to determine the slope back to residual crush
    # model assumes vehicles are in contact at t = 0, dx = 0
    # assumes equal weight distribution on all four tires

    i = 0

    # main loop will run when vehicles are engaged (spring is compressed)
    closing = 1       #  1 if vehicles are closing together, 0 after common velocity is met
    kreturn = np.nan  # initial values of nan
    dxperm = np.nan   # initial values of nan
    stop = 0
    print("")
    print('Model Initiated ============>')
    while stop == 0:
        if v2_initial >= v1_initial:
            print('Vehicles are separating at onset: Stopping Model')
            stop = 1
            break

        t = i * dt_impact

        if i == 0:

            # initial positions
            x1 = 0
            x2 = 0
            dx = x2 - x1

            # Initial Velocity - convert mph to fps
            v1 = v1_initial * 1.46667
            v2 = v2_initial * 1.46667

            # Initial Brake Applied - max available braking force
            v1_brakeFApp = v1_brake * W1 * mu_max
            v2_brakeFApp = v2_brake * W2 * mu_max

            #print(f'Brake Force Applied by V1 = {v1_brakeFApp} lb')
            #print(f'Brake Force Applied by V2 = {v2_brakeFApp} lb')

            # Initial Brake Force opposing vehicle velocity
            v1_brakeF = v1_brakeFApp * -1 * sign(v1)   # Initial brake force
            v2_brakeF = v2_brakeFApp * -1 * sign(v2)   # Initial brake force

            # Initial Acceleration - only due to braking
            a1 = v1_brakeF * 32.2 / W1
            a2 = v2_brakeF * 32.2 / W2

            springF = 0  # no initial spring force

            # store initial data in dataframe
            data = [t, x1, x2, v1, v2, a1, a2, springF, dx, v1_brakeF, v2_brakeF]
            spring_model = spring_model.append(pd.Series(data, index = columns), ignore_index=True)


        # this section will calculate forces based on closing or seperating phase
        if i > 0:

            # calculate vehicle motion [ft] based on prior velocity
            x1 = x1 + v1 * dt_impact
            x2 = x2 + v2 * dt_impact

            if closing == 1:
            # crush is equal to difference in vehicle motion during closing
                dx = x2 - x1
            elif (closing == 0) & ((x2-x1) < 1*dxperm):
            # crush is equal to the difference in vehicle motion until dxperm is reached
                dx = x2 - x1
            elif (closing == 0) & ((x2-x1) >= 1*dxperm):
            # crush remains at dxperm once vehicles seperate beyond dxperm
            # force should be zero at this point
                dx = dxperm

            # calculate vehicle velocity [ft/s] based on prior acceleration
            v1 = v1 + a1 * dt_impact
            v2 = v2 + a2 * dt_impact

            dx_past = spring_model.loc[i-1, 'dx']
            # check for closing / seperating status
            if closing == 1:
                if abs(dx_past) > abs(dx):  # if mutual crush decreased at current time step, vehicles are seperating
                    closing = 0
                    Fmax = spring_model.loc[i-1, 'springF']
                    dxmax = dx_past
                    dxperm = dxmax * (1 - cor**2)  # permanent crush
                    kreturn = Fmax / abs(dxmax - dxperm)  # return stiffness
                    print('===== Seperation ===========>')
                    print(f'Time (s) = {t}')
                    print(f'Peak Mutual Crush (in) = {dx_past *-12:.2f}')
                    print(f'Peak Force (lb) = {Fmax:.2f}')

            springF = SpringForce(dx, closing, k, input_k_disp, input_k_force, kreturn, dxperm)

            # calculate brake force based on applied braking and spring force
            # v1 brake force will always oppose v1 velocity
            v1_brakeF = v1_brakeFApp * -1 * sign(v1)
            v2_brakeF = BrakeCheck(v2_brakeFApp, springF, v2) # applied brake will oppose velocity if vehicle is in motion

            # calculate vehicle accleration [ft/s/s]
            a1 = 32.2 / W1 * (v1_brakeF - springF)
            a2 = 32.2 / W2 * (v2_brakeF + springF)

            if (closing == 0) & (dx >= dxperm) & (t >= tstop): # vehicles are seperating and dx is less than permanent crush
                stop = 1
                print("")
                print(f'========> Stopped t (s) = {t:.3f}')
                break

            # store initial data in dataframe
            data = [t, x1, x2, v1, v2, a1, a2, springF, dx, v1_brakeF, v2_brakeF]
            spring_model = spring_model.append(pd.Series(data, index = columns), ignore_index=True)

        i += 1

    return spring_model
