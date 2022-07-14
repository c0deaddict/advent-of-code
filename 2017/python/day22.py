from enum import Enum


class Dir(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class State(Enum):
    CLEAN = 0
    WEAKENED = 1
    INFECTED = 2
    FLAGGED = 3


DIR_ORDER = [Dir.UP, Dir.RIGHT, Dir.DOWN, Dir.LEFT]


def turn(dir, diff):
    return DIR_ORDER[(DIR_ORDER.index(dir) + diff) % len(DIR_ORDER)]


def turn_left(dir):
    return turn(dir, -1)


def turn_right(dir):
    return turn(dir, +1)


def reverse_dir(dir):
    return turn(dir, +2)


def move(dir, x, y):
    if dir == Dir.UP:
        return x, y - 1
    elif dir == Dir.RIGHT:
        return x + 1, y
    elif dir == Dir.DOWN:
        return x, y + 1
    elif dir == Dir.LEFT:
        return x - 1, y


def run_virus(states, pos, dir, bursts):
    num_infected = 0
    for i in range(bursts):
        s = states.get(pos, State.CLEAN)
        if s == State.INFECTED:
            dir = turn_right(dir)
            states.pop(pos)
        else:
            dir = turn_left(dir)
            states[pos] = State.INFECTED
            num_infected += 1

        pos = move(dir, *pos)

    return num_infected


def run_virus_pt2(states, pos, dir, bursts):
    num_infected = 0
    for i in range(bursts):
        s = states.get(pos, State.CLEAN)
        if s == State.CLEAN:
            dir = turn_left(dir)
            states[pos] = State.WEAKENED
        elif s == State.WEAKENED:
            states[pos] = State.INFECTED
            num_infected += 1
        elif s == State.INFECTED:
            dir = turn_right(dir)
            states[pos] = State.FLAGGED
        elif s == State.FLAGGED:
            dir = reverse_dir(dir)
            states.pop(pos)

        pos = move(dir, *pos)

    return num_infected


def make_states(grid):
    states = {}
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c:
                states[(x, y)] = State.INFECTED

    return states


def main():
    with open('../input/day22.input.txt') as f:
       grid = [[c == '#' for c in line.strip()] for line in f.readlines()]

    height = len(grid)
    width = len(grid[0])
    init_pos = (width // 2, height // 2)
    dir = Dir.UP
    init_states = make_states(grid)

    print(run_virus(dict(init_states), init_pos, dir, 10000))
    print(run_virus_pt2(dict(init_states), init_pos, dir, 10000000))


if __name__ == '__main__':
    main()
