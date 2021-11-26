from enum import Enum


class Dir(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


def get_cell(grid, x, y):
    try:
        return grid[y][x]
    except IndexError:
        return None


def is_empty(v):
    return v is None or v == ' '


def follow_path(grid, x, y, dir):
    letters = []
    steps = 0

    while True:
        c = get_cell(grid, x, y)
        if is_empty(c):
            return letters, steps

        steps += 1
        if c == '+':
            if dir in (Dir.UP, Dir.DOWN):
                if not is_empty(get_cell(grid, x-1, y)):
                    x = x-1
                    dir = Dir.LEFT
                else:
                    x = x+1
                    dir = Dir.RIGHT
            else:
                if not is_empty(get_cell(grid, x, y-1)):
                    y = y-1
                    dir = Dir.UP
                else:
                    y = y+1
                    dir = Dir.DOWN
        else:
            if c not in ('-', '|'):
                letters.append(c)

            if dir == Dir.UP:
                y = y-1
            elif dir == Dir.DOWN:
                y = y+1
            elif dir == Dir.LEFT:
                x = x-1
            elif dir == Dir.RIGHT:
                x = x+1


def main():
    grid = []
    with open('day19.input.txt') as f:
        for line in f.readlines():
            grid.append([c for c in line.rstrip('\n')])

    letters, steps = follow_path(grid, 1, 0, Dir.DOWN)
    print(''.join(letters))
    print(steps)


if __name__ == '__main__':
    main()
