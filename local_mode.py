from math import sqrt

def sdf_sphere(rx, ry, rz, shape):
    cx = shape["pos"][0]
    cy = shape["pos"][1]
    cz = shape["pos"][2]
    dist = sqrt((rx - cx)**2 + (ry - cy)**2 + (rz - cz)**2)
    return dist - shape["radius"]

def sdf_cylinder(rx, ry, rz, shape):
    cx = shape["pos"][0]
    cy = shape["pos"][1]
    cz = shape["pos"][2]
    radius = shape["radius"]
    height = shape.get("height")

    dxy = sqrt((rx - cx)**2 + (ry - cy)**2) - radius
    if height is None:
        return dxy

    dz = abs(rz - cz) - height / 2.0

    outside_x = max(dxy, 0.0)
    outside_z = max(dz, 0.0)
    outside = sqrt(outside_x**2 + outside_z**2)
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
    outside = sqrt(outside_x**2 + outside_y**2 + outside_z**2)
    inside = min(max(qx, qy, qz), 0.0)
    return outside + inside

def sdf_torus(rx, ry, rz, shape):
    cx = shape["pos"][0]
    cy = shape["pos"][1]
    cz = shape["pos"][2]
    R = shape["outer_radius"]
    r = shape["inner_radius"]
    dxy = sqrt((rx - cx)**2 + (ry - cy)**2) - R
    return sqrt(dxy**2 + (rz - cz)**2) - r


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

def norme(vx, vy, vz):
    length = sqrt(vx**2 + vy**2 + vz**2)
    if length == 0:
        return 0.0, 0.0, 0.0
    nx = vx / length
    ny = vy / length
    nz = vz / length
    return nx, ny, nz

def print_header(shapes, px, py, pz, vx, vy, vz):
    print(f"Rock thrown at the point ({px:.2f}, {py:.2f}, {pz:.2f}) and parallel to the vector ({vx:.2f}, {vy:.2f}, {vz:.2f})")
    for s in shapes:
        spx = s["pos"][0]
        spy = s["pos"][1]
        spz = s["pos"][2]
        if s["type"] == "sphere":
            print(f"Sphere of radius {s['radius']:.2f} at position ({spx:.2f}, {spy:.2f}, {spz:.2f})")
        elif s["type"] == "cylinder":
            h = s.get("height")
            if h is None:
                print(f"Cylinder of radius {s['radius']:.2f} and infinite height at position ({spx:.2f}, {spy:.2f}, {spz:.2f})")
            else:
                print(f"Cylinder of radius {s['radius']:.2f} and height {h:.2f} at position ({spx:.2f}, {spy:.2f}, {spz:.2f})")
        elif s["type"] == "box":
            sx = s["sides"][0]
            sy = s["sides"][1]
            sz = s["sides"][2]
            print(f"Box of dimensions ({sx:.2f}, {sy:.2f}, {sz:.2f}) at position ({spx:.2f}, {spy:.2f}, {spz:.2f})")
        elif s["type"] == "torus":
            print(f"Torus of inner radius {s['inner_radius']:.2f} and outer radius {s['outer_radius']:.2f} at position ({spx:.2f}, {spy:.2f}, {spz:.2f})")

def run_local(shapes, pos, vel):
    px = float(pos[0])
    py = float(pos[1])
    pz = float(pos[2])
    vx = float(vel[0])
    vy = float(vel[1])
    vz = float(vel[2])

    print_header(shapes, px, py, pz, vx, vy, vz)
    print()
    dx, dy, dz = norme(vx, vy, vz)
    if dx == 0 and dy == 0 and dz == 0:
        print()
        print("Result: Steps limit reached")
        return
    step = 1
    while step <= 1000:
        dist, nearest = find_closest(px, py, pz, shapes)
        if dist <= 0.1:
            print()
            print(f"Result: Intersection with {nearest['name']}")
            return

        px = px +dx * dist
        py = py + dy * dist
        pz = pz + dz * dist
        print(f"Step {step}: ({px:.2f}, {py:.2f}, {pz:.2f})")

        if dist > 1000.0:
            print()
            print("Result: Out of scene")
            return


        step += 1
    print()
    print("Result: Steps limit reached")