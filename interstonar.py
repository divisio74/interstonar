import argparse
import sys
import numpy as np

from parser import load_global, load_local
from global_mode import global_main_core, rock_mass

def main():
    parser = argparse.ArgumentParser(description="Rock simulator")
    parser.add_argument("--global", dest="is_global", action="store_true")
    parser.add_argument("--local",  dest="is_local",  action="store_true")
    parser.add_argument("config_file")
    parser.add_argument("-d", "--delta", type=float)
    parser.add_argument("Px", type=float)
    parser.add_argument("Py", type=float)
    parser.add_argument("Pz", type=float)
    parser.add_argument("Vx", type=float)
    parser.add_argument("Vy", type=float)
    parser.add_argument("Vz", type=float)
    args = parser.parse_args()

    if args.is_global and args.is_local:
        print("error : you cannot put the two mod at the same time", file=sys.stderr)
        sys.exit(1)
    if not args.is_global and not args.is_local:
        print("error : you have to choose a mod", file=sys.stderr)
        sys.exit(1)

    pos = np.array([args.Px, args.Py, args.Pz], dtype=float)
    vel = np.array([args.Vx, args.Vy, args.Vz], dtype=float)

    if args.is_global:
        if args.delta is None:
            print("error : you have to put the --delta arg with this mod", file=sys.stderr)
            sys.exit(1)
        bodies = load_global(args.config_file)
        rock = {
            "name": "rock",
            "mass": rock_mass,
            "pos": list(pos),
            "vel": list(vel)
        }
        global_main_core(rock, bodies, args.delta)
    else:
        shapes = load_local(args.config_file)
        print("Mode: local")
        print("Rock pos:", pos)
        print("Rock vel:", vel)
        print("Shapes loaded:", len(shapes))

if __name__ == "__main__":
    main()
