import os
from math import sqrt
import numpy as np

G = 6.67430e-11

def calcul(p1, p2, m1, m2):
    rx = p2[0] - p1[0]
    ry = p2[1] - p1[1]
    rz = p2[2] - p1[2]
    r = sqrt(rx**2 + ry**2 + rz**2)

    f = G * ((m1 * m2) / r**2)
    x = rx / r
    y = ry / r
    z = rz / r
    fx = f * x
    fy = f * y
    fz = f * z
    return fx, fy, fz

if __name__ == "__main__":
    p2 = np.array([0, 0, 6_371_000], dtype=float)
    p1 = np.array([0, 0, 0],         dtype=float)
    print(calcul(p1, p2, 70, 5.972e24))


