# various equations for reconstruction
import numpy as np

def b1values(bo, L, C, W):
    """
    calculate b1 given bo, damage length (L), damage depth (C) and vehicle weight (W)
    calculate b1 and bo values
    bo = damage offset speed (mph)
    b1 = slope of barrier impact speed and residual crush (mph/in)
    L = with of direct damage
    w = vehicle weight
    """

    return -1 * bo / C + np.sqrt((bo**2 + 2))


def ABfrombob1(W, bo, b1, L):
    """
    return A and B stiffness values from Weight, b0, b1 and damage length (L)
    calculate A anb B values from bo and b1
    L = damage length [in]
    W = vehicle weigth [lb]
    bo = damage offset speed [mph]
    b1 = slope of BEV - residual crush [mph/in]
    """

    A = 0.802 * W * bo * b1 / L
    B = 0.802 * W * b1**2 / L
    return [A, B]

def CrushEnergyAB(A, B, L, C):
    """
    crush energy [in-lb] from A and B values
    L - crush length [in]
    C - average crush depth  [in]
    """
    return L * (A*C + (B * C**2 / 2) + (A**2 / (2*B)))

def CrushForceAB(A, B, L, C):
    """
    calculate force from crush using A and B
    A [lb/in]
    B [lb/in/in]
    L crush length [in]
    C crush depth [in]
    """
    return L * (A + (B * C))

def StrikingDV(w1, w2, v1, v2, rest):
    """
    calculate striking vehicle delta-V [mph] given:
    w1, w2 - vehicle weights [lb]
    v1, v2 - striking / struck vehicle speeds [mph]
    rest - restitution
    """
    m1 = w1 / 32.2
    m2 = w2 / 32.2
    v1 = v1 * 1.46667
    v2 = v2 * 1.46667
    return (m2 / (m1 + m2) * (1 + rest) * (v1 - v2)) * 0.681818181818181

def StruckDV(w1, w2, v1, v2, rest):
    """
    calculate struck vehicle delta-V [mph] given:
    w1, w2 - vehicle weights [lb]
    v1, v2 - striking / struck vehicle speeds [mph]
    rest - restitution
    """
    m1 = w1 / 32.2
    m2 = w2 / 32.2
    v1 = v1 * 1.46667
    v2 = v2 * 1.46667
    return (m1 / (m1 + m2) * (1 + rest) * (v1 - v2)) * 0.681818181818181


def EnergyDV(w1, w2, Edis, cor):
    """
    see Rose SAE #2005-01-1200
    vehicle 1 and 2 delta-V [mph]
    Edis = dissipated energy [ft-lb]
    cor = coefficient of restitution
    """
    m1 = w1 / 32.2
    m2 = w2 / 32.2
    A = (m1 * m2) / (m1 + m2)
    B = (1 + cor) / (1 - cor)
    dv1 = (1/m1) * np.sqrt(A * 2 * B * Edis)
    dv2 = (1/m2) * np.sqrt(A * 2 * B * Edis)
    print(f'Delta-V in mph | v1: {dv1*0.681818181818181:0.2f}, v2: {dv2*0.681818181818181:0.2f}')
    return [dv1*0.681818181818181, dv2*0.681818181818181]

def formFactorin(crush_list_in):
    """
    crush_list is a list of 6 crush measurements [in]
    """
    cbar = [0] * len(crush_list_in)
    cbar[0] = crush_list_in[0]
    cbar[1] = crush_list_in[1] * 2
    cbar[2] = crush_list_in[2] * 2
    cbar[3] = crush_list_in[3] * 2
    cbar[4] = crush_list_in[4] * 2
    cbar[5] = crush_list_in[5]
    cbar = np.sum(cbar) / 10
    A = 1 / (15 * cbar**2)
    B = crush_list_in[0]**2 + crush_list_in[0]*crush_list_in[1] + 2*crush_list_in[1]**2 + crush_list_in[1]*crush_list_in[2]\
        + 2*crush_list_in[2]**2 + crush_list_in[2]*crush_list_in[3] + 2*crush_list_in[3]**2 + \
        crush_list_in[3]*crush_list_in[4] + 2*crush_list_in[4]**2 + crush_list_in[4]*crush_list_in[5] + crush_list_in[5]**2
    return A * B

def FrickeEfromAB(A, B, L, crush_list, theta=0):
    """
    crush_list in inches
    """
    G = A**2 / (2 * B)
    print(f'G: {G}')
    print(f'Angle Correction = {(1+np.tan(theta)**2)}')
    one = (5 * G) + A/2 * (crush_list[0] + 2 * crush_list[1] + 2 * crush_list[2] + 2 * crush_list[3] + 2 * crush_list[4] + crush_list[5])
    two = (B / 6) * (crush_list[0]**2 + 2*crush_list[1]**2 + 2*crush_list[2]**2 + 2*crush_list[3]**2 + 2*crush_list[4]**2 + crush_list[5]**2 +
                     crush_list[0] * crush_list[1] + crush_list[1] * crush_list[2] + crush_list[2] * crush_list[3] + crush_list[3] * crush_list[4] +
                     crush_list[4] * crush_list[5])
    return (L / 5) * (one + two) * (1+np.tan(theta)**2)
    
def BarrierCrushEnergy(W, s):
    """
    W [lb] = weight of test vehicle
    s [mph] = barrier impact speed
    """
    return 0.5 * (W/32.2) * (s*1.46667)**2

def cipriani_rest(ClosingSpeed):
    """
    calculate restitution based on closing speed in mph
    based on regression performed by Cipriani
    Cipriani, A., et al. (2002). "Low Speed Collinear Impact Severity: A Comparison Between Full Scale Testing and Analytical Prediction Tools with Restitution Analysis."
    Society of Automotive Engineers 2002-01-0540.
    """

    A = 0.47477
    B = 0.26139 * np.log10(abs(ClosingSpeed) * 0.44704)
    C = 0.03382 * np.log10(abs(ClosingSpeed) * 0.44704)**2
    D = 0.11639 * np.log10(abs(ClosingSpeed) * 0.44704)**3
    return A - B + C - D

def CrushEnergyInt(dx, f):
    """
    calculate dissipated energy from force-deformation data
    dx [ft]
    f [lb]
    """

    return np.trapz(f, x=dx)

def SpringSeriesKeff(k1, k2):
    """
    calcualte effective stiffness for two springs in series
    """

    return 1 / (1/k1 + 1/k2)

def BEVfromE(W, E):
    """
    calculate Barrier Equivalent Velocity [mph] from Energy [ft/lb]
    """
    return np.sqrt(2*E/(W/32.2)) * 0.681818
