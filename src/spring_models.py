"""
The spring model used can vary depending on the user Inputs
Additional spring models can be created here, all inputs need to remain the same across all functions
to preserve functinality 
"""

# Spring force from two lists
def SpringFdx(dx, closing, k, input_k_disp, input_k_force, kreturn, dxperm):
    """
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
    k - spring stiffness [lb/in]
    input_k_disp - unused
    input_k_force - unused
    """
    if dx >= 0:
        return 0

    if closing == 1:
        return k * abs(dx) * 12

    if (closing == 0) & ((dx - dxperm) < 0): # closing and dx has not reached dxperm
        return kreturn * abs(dx - dxperm)

    if (closing == 0) & ((dx - dxperm) >= 0): # closing and dx is less than dxperm
        return 0
