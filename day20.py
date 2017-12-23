import re
from collections import namedtuple

Vec = namedtuple('Vec', 'x y z')
Particle = namedtuple('Particle', 'id p v a')


def parse_particle(id, line):
    parts = dict()
    for m in re.finditer('([pva])=<(-?\d+),(-?\d+),(-?\d+)>', line):
        parts[m.group(1)] = Vec(x=int(m.group(2)),
                                y=int(m.group(3)),
                                z=int(m.group(4)))
    return Particle(id=id, **parts)


def distance(p):
    return abs(p.x) + abs(p.y) + abs(p.z)


def main():
    with open('day20.input.txt') as f:
        particles = [parse_particle(i, line) for i, line in enumerate(f.readlines())]

        def sort_key(p):
            return distance(p.a), distance(p.v), distance(p.p)

        particles.sort(key=sort_key)
        print(particles[0].id)


if __name__ == '__main__':
    main()
