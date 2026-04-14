import os
from math import sqrt
import numpy as np

G = 6.67430e-11
rock_mass = 1000
max_try = 1000

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
        tfx, tfy, tfz = Calcul(a["pos"], b ["pos"], a["mass"], b["mass"])
        fx += tfx
        fy += tfy
        fz += tfz
        pass
    return fx, fy, fz


def euler_calcul(bodies, dt):
    Force_Tab = []
    for b in bodies:
        Force_Tab.append(CalculForAll(b, bodies))
    for i in range(len(bodies)):
        c = bodies[i]
        fx, fy, fz = Force_Tab[i]
        accel_x = fx / c["mass"]
        accel_y = fy / c["mass"]
        accel_z = fz /c["mass"]
        vitesse_x = c["vel"][0]
        vitesse_y = c["vel"][1]
        vitesse_z = c["vel"][2]
        new_vitesse_x = vitesse_x + (accel_x * dt)
        new_vitesse_y = vitesse_y + (accel_y * dt)
        new_vitesse_z = vitesse_z + (accel_z * dt)
        c["pos"][0] = c["pos"][0] + (new_vitesse_x * dt)
        c["pos"][1] = c["pos"][1] + (new_vitesse_y * dt)
        c["pos"][2] = c["pos"][2] + (new_vitesse_z * dt)
        c["vel"][0] = new_vitesse_x
        c["vel"][1] = new_vitesse_y
        c["vel"][2] = new_vitesse_z

def rock_end(bodies, rock):
    for b in bodies:
        diff = rock["pos"] - b["pos"]
        distance = sqrt(diff[0]**2 + diff[1]**2 + diff[2]**2)
        if distance <= b["radius"]:
            return b
    return None

def body_fusion(bodies):
    return None





if __name__ == "__main__":
    from parser import load_global
    bodies = load_global("global_scene_example.toml")

    rock1 = {"pos": bodies[0]["pos"].copy()}
    print("Test 1:", rock_end(bodies, rock1))

    rock2 = {"pos": np.array([1e20, 1e20, 1e20])}
    print("Test 2:", rock_end(bodies, rock2))



