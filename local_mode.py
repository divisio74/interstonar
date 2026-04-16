import os
from math import sqrt

def sdf_sphere(rx, ry, rz, shape):
    cx = shape["pos"][0]
    cy = shape["pos"][1]
    cz = shape["pos"][2]
    dist = math.sqrt((rx - cx)**2 + (ry - cy)**2 + (rz - cz)**2)
    return dist - shape["radius"]

def sdf_cylinder(rx, ry, rz, shape):
    cx = shape["pos"][0]
    cy = shape["pos"][1]
    cz = shape["pos"][2]
    radius = shape["radius"]
    height = shape.get("height")

    dxy = math.sqrt((rx - cx)**2 + (ry - cy)**2) - radius

    if height is None:
        return dxy

    dz = abs(rz - cz) - height / 2.0

    outside_x = max(dxy, 0.0)
    outside_z = max(dz, 0.0)
    outside = math.sqrt(outside_x**2 + outside_z**2)
    inside = min(max(dxy, dz), 0.0)
    return outside + inside

def sdf_box(rx, ry, rz, shape):
    cx = shape["pos"][0]
    cy = shape["pos"][1]
    cz = shape["pos"][2]
    hx = shape["sides"][0] / 2.0
    hy = shape["sides"][1] / 2.0
    hz = shape["sides"][2] / 2.0

    qx = abs(rx - cx) - hx
    qy = abs(ry - cy) - hy
    qz = abs(rz - cz) - hz

    outside_x = max(qx, 0.0)
    outside_y = max(qy, 0.0)
    outside_z = max(qz, 0.0)
    outside = math.sqrt(outside_x**2 + outside_y**2 + outside_z**2)
    inside = min(max(qx, qy, qz), 0.0)
    return outside + inside

def sdf_torus(rx, ry, rz, shape):
    cx = shape["pos"][0]
    cy = shape["pos"][1]
    cz = shape["pos"][2]
    R = shape["outer_radius"]
    r = shape["inner_radius"]
    dxy = math.sqrt((rx - cx)**2 + (ry - cy)**2) - R
    return math.sqrt(dxy**2 + (rz - cz)**2) - r


def get_sdf(rx, ry, rz, shape):
    t = shape["type"]
    if t == "sphere":
        return sdf_sphere(rx, ry, rz, shape)
    elif t == "cylinder":
        return sdf_cylinder(rx, ry, rz, shape)
    elif t == "box":
        return sdf_box(rx, ry, rz, shape)
    elif t == "torus":
        return sdf_torus(rx, ry, rz, shape)


def find_closest(rx, ry, rz, shapes):
    best_dist = float("inf")
    best_shape = None
    for s in shapes:
        d = get_sdf(rx, ry, rz, s)
        if d < best_dist:
            best_dist = d
            best_shape = s
    return best_dist, best_shape

def run_local(shapes, pos, vel):
    px = float(pos[0])
    py = float(pos[1])
    pz = float(pos[2])
    vx = float(vel[0])
    vy = float(vel[1])
    vz = float(vel[2])

    nearest = find_closest(px, py, pz, shapes)