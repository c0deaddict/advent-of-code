import re
from collections import namedtuple, defaultdict

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


def vec_add(a, b):
    return Vec(x=a.x + b.x, y=a.y + b.y, z=a.z + b.z)


def move(p):
    v = vec_add(p.v, p.a)
    return Particle(id=p.id,
                    p=vec_add(p.p, v),
                    v=v,
                    a=p.a)


def tick(particles):
    return [move(p) for p in particles]


def remove_collisions(particles):
    taken = defaultdict(list)
    for p in particles:
        taken[p.p].append(p)

    return [lst[0] for lst in taken.values() if len(lst) == 1]


def simulate(particles):
    for i in range(0, 2000):
        particles = tick(remove_collisions(particles))
    return particles


def main():
    with open('../input/day20.input.txt') as f:
        particles = [parse_particle(i, line) for i, line in enumerate(f.readlines())]

        def sort_key(p):
            return distance(p.a), distance(p.v), distance(p.p)

        particles.sort(key=sort_key)
        print(particles[0].id)

        print(len(simulate(particles)))


if __name__ == '__main__':
    main()
