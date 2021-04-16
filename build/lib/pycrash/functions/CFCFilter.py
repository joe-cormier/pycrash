from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

def cfcfilt(CFC, data, dt):
    """
    Create filter using CFC based on SAE J211
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.filtfilt.html
    """
    wd = 2 * 3.14159 * CFC * 2.0775
    wa = (np.sin(wd * dt / 2)) / (np.cos(wd * dt / 2))
    aO = (wa**2) / (1 + wa * (2**0.5) + wa**2)
    a1 = 2 * aO
    a2 = aO
    b1 = -2 * ((wa**2) - 1) / (1 + wa * (2**0.5) + wa**2)
    b2 = (-1 + wa * (2**0.5) - wa**2) / (1 + wa * (2**0.5) + wa**2)
    A = [1, -b1, -b2]
    B = [aO, a1, a2]
    filteredData = signal.filtfilt(B, A, data)
    return filteredData
