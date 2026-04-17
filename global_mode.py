from math import sqrt

G = 6.674e-11
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
        c["pos"][0] = c["pos"][0] + (vitesse_x * dt)
        c["pos"][1] = c["pos"][1] + (vitesse_y * dt)
        c["pos"][2] = c["pos"][2] + (vitesse_z * dt)
        c["vel"][0] = vitesse_x + (accel_x * dt)
        c["vel"][1] = vitesse_y + (accel_y * dt)
        c["vel"][2] = vitesse_z + (accel_z * dt)

def euler_rock(rock, bodies):
    fx, fy, fz = CalculForAll(rock, bodies)
    ax = fx / rock["mass"]
    ay = fy / rock["mass"]
    az = fz / rock["mass"]
    return ax, ay, az

def euler_rock_apply(rock, accel, dt):
    ax, ay, az = accel
    rock["pos"][0] += rock["vel"][0] * dt
    rock["pos"][1] += rock["vel"][1] * dt
    rock["pos"][2] += rock["vel"][2] * dt
    rock["vel"][0] += ax * dt
    rock["vel"][1] += ay * dt
    rock["vel"][2] += az * dt

def rock_end(rock, bodies):
    for b in bodies:
        diffx = rock["pos"][0] - b["pos"][0]
        diffy = rock["pos"][1] - b["pos"][1]
        diffz = rock["pos"][2] - b["pos"][2]
        distance = sqrt(diffx**2 + diffy**2 + diffz**2)
        if distance <= b["radius"]:
            return b
    return None

def body_fusion(bodies):
    cluster = []

    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            diffx = bodies[i]["pos"][0] - bodies[j]["pos"][0]
            diffy = bodies[i]["pos"][1] - bodies[j]["pos"][1]
            diffz = bodies[i]["pos"][2] - bodies[j]["pos"][2]
            distance = sqrt(diffx**2 + diffy**2 + diffz**2)
            if distance <= bodies[i]["radius"] + bodies[j]["radius"]:
                in_the_cluster = 0
                for k in cluster:
                    if i in k or j in k:
                        if i in k:
                            k.add(j)
                        elif j in k:
                            k.add(i)
                        in_the_cluster = 1
                        break
                if in_the_cluster == 0:
                    cluster.append({i, j})
    if len(cluster) == 0:
        return bodies
    return internal_body_fusion(bodies, cluster)


def is_in_cluster(i, clusters):
    for c in clusters:
        if i in c:
            return True
    return False


def internal_body_fusion(bodies, clusters):
    new_bodies = []

    for c in clusters:
        mass_total = 0
        radius_total = 0
        vitesse_total = 0
        nom_total = []
        nvx, nvy, nvz = 0, 0, 0
        npx, npy, npz = 0, 0, 0
        cluster = [bodies[idx] for idx in c]
        for b in cluster:
            mass_total += b["mass"]
        for b in cluster:
            radius_total += b["radius"] ** 3
        new_radius = radius_total ** (1/3)
        for b in cluster:
            nvx += b["mass"] * b["vel"][0]
            nvy += b["mass"] * b["vel"][1]
            nvz += b["mass"] * b["vel"][2]
        nvx /= mass_total
        nvy /= mass_total
        nvz /= mass_total
        for b in cluster:
            vitesse = sqrt(b["vel"][0]**2 + b["vel"][1]**2 + b["vel"][2]**2)
            npx += vitesse * b["pos"][0]
            npy += vitesse * b["pos"][1]
            npz += vitesse * b["pos"][2]
            vitesse_total += vitesse
        npx /= vitesse_total
        npy /= vitesse_total
        npz /= vitesse_total
        for b in cluster:
            nom_total.append(b["name"])
        new_name = "-".join(sorted(nom_total))
        new_body = {
            "name": new_name,
            "mass": mass_total,
            "radius": new_radius,
            "pos": [npx, npy, npz],
            "vel": [nvx, nvy, nvz]
        }
        new_bodies.append(new_body)

    for i in range(len(bodies)):
        if not is_in_cluster(i, clusters):
            new_bodies.append(bodies[i])
    return new_bodies

def global_main_core(rock, bodies, dt):
    i = 0
    print("Rock coordinates (x y z) are:")
    while (i < 1000):
        px = format(round(rock["pos"][0]), ",")
        py = format(round(rock["pos"][1]), ",")
        pz = format(round(rock["pos"][2]), ",")
        print("t = %i: (%s %s %s)" % (i, px, py, pz))
        is_end = rock_end(rock, bodies)
        if (is_end != None):
            print("Collision between rock and %s" % is_end["name"])
            print("Mission success")
            return is_end
        accel = euler_rock(rock, bodies)
        euler_calcul(bodies, dt)
        euler_rock_apply(rock, accel, dt)
        bodies = body_fusion(bodies)
        i += 1
    print("Mission failure")
    return 0


if __name__ == "__main__":
    bodies = [
        {"name": "Charlie", "mass": 1e20, "radius": 100,
         "pos": [0, 0, 0], "vel": [1, 0, 0]},
        {"name": "Alpha",   "mass": 1e20, "radius": 100,
         "pos": [50, 0, 0], "vel": [1, 0, 0]},
        {"name": "Bravo",   "mass": 1e20, "radius": 100,
         "pos": [0, 50, 0], "vel": [1, 0, 0]},
    ]
    fusion = body_fusion(bodies)
    print("Nom fusioné :", [b["name"] for b in fusion])




