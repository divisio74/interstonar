import os
from math import sqrt
import numpy as np

G = 6.67430e-11

def Calcul(p1, p2, m1, m2):
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

def CalculForAll(a, bodies):
    fx, fy, fz = 0.0, 0.0, 0.0
    for b in bodies:
        if b is a:
            continue
        tfx, tfy, tfz += Calcul(a["pos"], b ["pos"], a["mass"], b["mass"])
        fx += tfx
        fy += tfy
        fz += tfz
        pass
    return fx, fy, fz


if __name__ == "__main__":
    from parser import load_global
    bodies = load_global("global_scene_example.toml")

    for body in bodies:
        f = CalculForAll(body, bodies)
        print(f"Force totale sur {body['name']:8s} = {f}")



