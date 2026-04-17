import tomllib

def to_vec(d):
    return [float(d["x"]), float(d["y"]), float(d["z"]) ]


def read_toml(path):
    with open(path, "rb") as f:
        return tomllib.load(f)

def load_local(path):
    data = read_toml(path)

    counters = {"sphere": 0, "cylinder": 0, "box": 0, "torus": 0}
    shapes = []

    for entry in data["body"]:
        t = entry["type"]
        counters[t] += 1
        name = entry.get("name", f"{t.upper()}_{counters[t]}")

        shape = {
            "type": t,
            "name": name,
            "pos":  to_vec(entry["position"]),
        }

        if t == "sphere":
            shape["radius"] = float(entry["radius"])

        elif t == "cylinder":
            shape["radius"] = float(entry["radius"])
            shape["height"] = float(entry["height"]) if "height" in entry else None

        elif t == "box":
            shape["sides"] = to_vec(entry["sides"])

        elif t == "torus":
            shape["inner_radius"] = float(entry["inner_radius"])
            shape["outer_radius"] = float(entry["outer_radius"])

        else:
            raise ValueError(f"Unknown shape type: {t}")

        shapes.append(shape)

    return shapes

def load_global(path):
    data = read_toml(path)

    bodies = []
    for entry in data["body"]:
        bodies.append({
            "name":   entry["name"],
            "mass":   float(entry["mass"]),
            "radius": float(entry["radius"]),
            "pos":    to_vec(entry["position"]),
            "vel":    to_vec(entry["direction"]),
        })
    return bodies




if __name__ == "__main__":
    print("local :")
    for s in load_local("testfile/local_scene_example.toml"):
        print(s)

    print("\nglobal :")
    for b in load_global("testfile/global_scene_example.toml"):
        print(b)


