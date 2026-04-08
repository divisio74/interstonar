import tomllib
import numpy as np


def read_toml(path):
    with open(path, "rb") as f:
        return tomllib.load(f)


if __name__ == "__main__":
    data = read_toml("local_scene_example.toml")
    print(data)
