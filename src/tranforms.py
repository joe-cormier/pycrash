"""
Tranformation functions
"""
import math
import numpy as np
# global frame to vehicle Frame
def GlobaltoVeh(pX, pY, theta):
    """
    theta - rotation angle in radians
    pX, pY - point coorinates in global frame
    """
    px = pX * math.cos(theta) + pY * math.sin(theta)
    py = -1 * pX * math.sin(theta) + pY * math.cos(theta)

    return np.array([x, y])

def VehtoGlobal(cg_x, cg_y, px, py, theta):
    """
    theta - heading angle in radians
    cg_x, cg_y, - linear translation of cg
    px, py - point coorinates in vehicle frame
    """

    X = px * math.cos(theta) - py * math.sin(theta)
    Y = px * math.sin(theta) + py * math.cos(theta)

    return np.array([X, Y])

theta = 90 * (math.pi/180)
GlobaltoVeh(theta, 0, 0, 10, 0)

VehtoGlobal(0, 0, 10, 0, theta)
