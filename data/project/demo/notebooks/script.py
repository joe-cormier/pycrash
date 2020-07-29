print('Hello from Script')
x = 1
y = 2
print(f'Summation = {x+y}')

import numpy as np

def cipriani(ClosingSpeed):
    # calculate restitution based on closing speed in mph
    # based on regression performed by Cipriani
    A = 0.47477
    B = -0.26139 * np.log(np.absolute(ClosingSpeed) * 0.44704)
    C = 0.03382 * np.log(np.absolute(ClosingSpeed) * 0.447704)**2
    D = -0.11639 * np.log(np.absolute(ClosingSpeed) * 0.44704)**3
    return A + B + C + D
#