# --- Part Two ---
#
# As a stress test on the system, the programs here clear the grid and then
# store the value 1 in square 1. Then, in the same allocation order as shown
# above, they store the sum of the values in all adjacent squares,
# including diagonals.
#
# So, the first few squares' values are chosen as follows:
#
# - Square 1 starts with the value 1.
# - Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
# - Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
# - Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values, 4.
# - Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.
#
# Once a square is written, its value does not change. Therefore, the first
# few squares would receive the following values:
#
# 147  142  133  122   59
# 304    5    4    2   57
# 330   10    1    1   54
# 351   11   23   25   26
# 362  747  806--->   ...
#
# What is the first value written that is larger than your puzzle input?
from math import sqrt, ceil


def solve(input):
    spiral = [1]

    while spiral[-1] < input:
        x, y = spiral_coords(len(spiral)+1)

        neighbours = [
            (x-1, y-1),
            (x-1, y),
            (x-1, y+1),
            (x,   y-1),
            (x,   y+1),
            (x+1, y-1),
            (x+1, y),
            (x+1, y+1),
        ]

        value = 0
        for nx, ny in neighbours:
            pos = spiral_pos(nx, ny) - 1
            if pos < len(spiral):
                value += spiral[pos]

        spiral.append(value)

    print(spiral[-1])


def spiral_coords(pos):
    size = ceil(sqrt(pos))
    start = 1 + (size-1)*(size-1)
    diff = pos - start
    r = size // 2
    if size % 2 == 0:
        if diff < size:
            # right
            x = r
            y = diff - (r-1)
        else:
            # top
            x = (r-1) - (diff - size)
            y = r
    else:
        if diff < size:
            # left
            x = -r
            y = r - diff
        else:
            # bottom
            x = (diff - size) - (r-1)
            y = -r

    return x, y


def spiral_pos(x, y):
    r = max(abs(x), abs(y))
    size = 1 + r*2
    start = (size-1)*(size-1) - (size-2)*2
    end = size*size

    if x == r:
        if y == -r:
            return end
        else:
            # right
            return start + (r-1) + y
    elif x == -r:
        # left
        return start + (size-2)*2+1 + r - y
    elif y == r:
        # top
        return start + (size-1) + (r-1) - x
    elif y == -r:
        # bottom
        return end + x - r


print(solve(361527))
