
import numpy as np

# Spring force from two lists
def SpringFdx(dx, closing, k, input_k_disp, input_k_force, kreturn, dxperm):
    """
    spring force using lookup table of displacement [ft], force [lb]
    input_k_disp from model - [ft]
    input_k_force from input - [lb]
    k - unused
    """
    if dx >= 0:
        return 0

    if closing == 1:
        return np.interp(-1*dx, input_k_disp, input_k_force)

    if (closing == 0) & ((dx - dxperm) < 0): # seperating and dx has not reached dxperm
        return kreturn * abs(dx - dxperm)

    if (closing == 0) & ((dx - dxperm) >= 0): # seperating and dx is less than dxperm
        return 0

# calculate force based on current mutual crush
def SpringForce(dx, closing, k, input_k_disp, input_k_force, kreturn, dxperm):
    """
    Spring force using linear spring assumption
    k - spring stiffness [lb/ft]
    input_k_disp - unused
    input_k_force - unused
    """
    if dx >= 0:
        return 0

    if closing == 1:
        return k * abs(dx)

    if (closing == 0) & ((dx - dxperm) < 0): # closing and dx has not reached dxperm
        return kreturn * abs(dx - dxperm)

    if (closing == 0) & ((dx - dxperm) >= 0): # closing and dx is less than dxperm
        return 0
