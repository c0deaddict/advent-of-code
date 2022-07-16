# --- Day 11: Hex Ed ---
#
# Crossing the bridge, you've barely reached the other side of the stream when a program comes up to you, clearly in
# distress. "It's my child process," she says, "he's gotten lost in an infinite grid!"
#
# Fortunately for her, you have plenty of experience with infinite grids.
#
# Unfortunately for you, it's a hex grid.
#
# The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be found to the north, northeast,
# southeast, south, southwest, and northwest:
#
#   \ n  /
# nw +--+ ne
#   /    \
# -+      +-
#   \    /
# sw +--+ se
#   / s  \
#
# You have the path the child process took. Starting where he started, you need to determine the fewest number of steps
# required to reach him. (A "step" means to move from the hex you are in to any adjacent hex.)
#
# For example:
#
#     ne,ne,ne is 3 steps away.
#     ne,ne,sw,sw is 0 steps away (back where you started).
#     ne,ne,s,s is 2 steps away (se,se).
#     se,sw,se,sw,sw is 3 steps away (s,s,sw).
#
# --- Part Two ---
#
# How many steps away is the furthest he ever got from his starting position?


def step(pos, dir):
    x, y = pos
    if dir == "n":
        return x, y - 2
    elif dir == "ne":
        return x + 1, y - 1
    elif dir == "nw":
        return x - 1, y - 1
    elif dir == "s":
        return x, y + 2
    elif dir == "sw":
        return x - 1, y + 1
    elif dir == "se":
        return x + 1, y + 1
    else:
        raise ValueError("unknown dir: %s" % dir)


def walk(steps):
    pos = (0, 0)
    path = []
    for dir in steps:
        pos = step(pos, dir)
        path.append(pos)
    return path


def shortest_path(pos):
    x, y = pos
    w = abs(x)
    h = abs(y) - abs(x)
    return w + h // 2


def main():
    with open("../input/day11_1.input.txt") as f:
        steps = f.read().split(",")
        path = walk(steps)
        print(shortest_path(path[-1]))
        print(max(map(shortest_path, path)))


if __name__ == "__main__":
    main()
