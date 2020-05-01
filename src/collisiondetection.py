
"""
Earth Frame to get relative coorinates of vehicles and reference points on vehicles
Transform to Vehicle 2 to test for contact by Vehicle 1

Impulse Momentum -
Allow contact point P1 (Vehicle 1) and contact edge E2 (Vehicle 2) to be pre chosen

Force - Deflection (A/B values)
Allow contact edges E1, E2, to be pre chosen.  Breakdown each edge into points




calculate closing velocity at every time step
if closing velocity is negative, vehicles are moving away from each other and
collision detection function won't run

if closing speed is positive, direction of closing speed with respect to
each vehicle's coorindate system will determine which edge to monitor

If closing speed vector lies on a vertex, then that single point is monitored for that time step
    - maybe use different stiffness values?



"""
import numpy as np
import math
# Vehicle velocity in Global coorindate system
Vx1 = 10
Vy1 = 0

Vx2 = 0
Vy2 = 0

V1 = np.array([Vx1, Vy1])
V2 = np.array([Vx2, Vy2])

# Closing velocity
V_Closing = V1 - V2
Theta_Closing_rad = math.atan2(V_Closing[1], V_Closing[0])  # rad
Theta_Closing_deg = Theta_Closing_rad * 180/math.pi

print(f'Closing Speed in Global Frame = {V_Closing}')
print(f'Closing Angle in Global Frame = {Theta_Closing_deg:.2} deg')

"""
Vehicle positions with respect to each other
P1, P2 can be points chosen by user to determine when contact is made
"""
Px1 = 0
Py1 = 0

Px2 = 30
Py2 = 0

P1 = np.array([Px1, Py1])
P2 = np.array([Px2, Py2])

P_Relative = P1 - P2
Theta_Relative_rad = math.atan2(P_Relative[1], P_Relative[0])  # rad
Theta_Relative_deg = Theta_Relative_rad * 180/math.pi

print(f'Reltive Position in Global Frame = {P_Relative}')
print(f'Relative Angle in Global Frame = {Theta_Relative_deg:.2f} deg')
