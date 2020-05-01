"""
Tranformation functions
"""
import math
import numpy as np
# global frame to vehicle Frame
def GlobaltoVeh(theta, X, Y):
    """
    theta - rotation angle in radians
    X, Y - point coorinates in global frame
    """
    x = X * math.cos(theta) + Y * math.sin(theta)
    y = -1 * X * math.sin(theta) + Y * math.cos(theta)

    return np.array([x, y])

def VehtoGlobal(theta, x, y):
    """
    theta - rotation angle in radians
    x, y - point coorinates in vehicle frame
    """

    X = x * math.cos(theta) - y * math.sin(theta)
    Y = x * math.sin(theta) + y * math.cos(theta)

    return np.array([X, Y])

theta = 180 * (math.pi/180)
GlobaltoVeh(theta, 10, 0)

VehtoGlobal(theta, -10, 0)
