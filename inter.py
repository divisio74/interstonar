import os
from math import sqrt

G = 6.67430e-11

p1 = (1,2) # en m
p2 = (2,1)
m1 = 70 # en Kg
m2 = 5.972e24


def calcul(G, p1, p2, m1, m2):
    rx = p2[0] - p1[0]
    ry = p2[1] - p1[1]
    r = sqrt(rx**2 + ry**2)

    f = G * ((m1 * m2) / r**2)
    x = rx / r
    y = ry / r
    fx = f * x
    fy = f * y
    return fx, fy

print(calcul(G, p1, p2, m1, m2))



