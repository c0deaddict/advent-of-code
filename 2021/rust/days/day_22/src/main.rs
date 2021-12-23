use itertools::Itertools;
use lib::run;
use regex::Regex;
use std::{cmp, collections::HashSet};

#[derive(Debug, Hash, Eq, PartialEq, Copy, Clone)]
struct Position {
    x: i32,
    y: i32,
    z: i32,
}

enum Axis {
    X,
    Y,
    Z,
}

#[derive(Debug, Hash, Eq, PartialEq, Copy, Clone)]
struct Cube {
    min: Position,
    max: Position,
}

struct Action {
    cube: Cube,
    state: bool,
}

type Input = Vec<Action>;

impl Position {
    fn new(x: i32, y: i32, z: i32) -> Self {
        Self { x, y, z }
    }

    fn get(&self, axis: &Axis) -> i32 {
        match axis {
            Axis::X => self.x,
            Axis::Y => self.y,
            Axis::Z => self.z,
        }
    }
}

impl Cube {
    fn new(min: Position, max: Position) -> Self {
        if max.x < min.x || max.y < min.y || max.z < min.z {
            panic!("max < min");
        }

        Self { min, max }
    }

    /// Does self overlap with other?
    fn overlaps_with(&self, other: &Self) -> bool {
        self.max.x < other.min.x
            || self.max.y < other.min.y
            || self.max.z < other.min.z
            || self.min.x > other.max.x
            || self.min.y > other.max.y
            || self.min.z > other.max.z
    }

    /// Is self contained in other?
    fn is_contained_in(&self, other: &Self) -> bool {
        self.min.x >= other.min.x
            && self.max.x <= other.max.x
            && self.min.y >= other.min.y
            && self.max.y <= other.max.y
            && self.min.z >= other.min.z
            && self.max.z <= other.max.z
    }

    /// Intersection of self with other. This is commutative.
    fn intersect(&self, other: &Self) -> Option<Self> {
        if self.overlaps_with(&other) {
            // no intersection.
            None
        } else {
            let min = Position {
                x: cmp::max(self.min.x, other.min.x),
                y: cmp::max(self.min.y, other.min.y),
                z: cmp::max(self.min.z, other.min.z),
            };
            let max = Position {
                x: cmp::min(self.max.x, other.max.x),
                y: cmp::min(self.max.y, other.max.y),
                z: cmp::min(self.max.z, other.max.z),
            };
            Some(Cube::new(min, max))
        }
    }

    /// Subtract other from self.
    fn subtract(&self, other: &Self) -> Vec<Self> {
        if self.overlaps_with(&other) {
            vec![self.clone()]
        } else if self.is_contained_in(&other) {
            vec![]
        } else {
            let splits = [Axis::X, Axis::Y, Axis::Z].map(|i| {
                let mut parts = vec![];
                let mut start = self.min.get(&i);
                if other.min.get(&i) > self.min.get(&i) {
                    parts.push((start, other.min.get(&i) - 1));
                    start = other.min.get(&i);
                }
                if other.max.get(&i) < self.max.get(&i) {
                    parts.push((start, other.max.get(&i)));
                    start = other.max.get(&i) + 1;
                }
                parts.push((start, self.max.get(&i)));
                return parts;
            });

            splits[0]
                .iter()
                .cartesian_product(&splits[1])
                .cartesian_product(&splits[2])
                .map(|(((x1, x2), (y1, y2)), (z1, z2))| {
                    let min = Position::new(*x1, *y1, *z1);
                    let max = Position::new(*x2, *y2, *z2);
                    Cube::new(min, max)
                })
                .filter(|c| !c.is_contained_in(&other))
                .collect()
        }
    }

    fn volume(&self) -> u64 {
        let sx = (self.max.x - self.min.x + 1) as u64;
        let sy = (self.max.y - self.min.y + 1) as u64;
        let sz = (self.max.z - self.min.z + 1) as u64;
        return sx * sy * sz;
    }
}

fn parse_input(input: &str) -> Input {
    let re =
        Regex::new(r"^(off|on) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)$").unwrap();

    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| {
            let c = re.captures(l).unwrap();
            let mut it = c.iter().skip(1);
            let state = it.next().unwrap().unwrap().as_str() == "on";
            let (x1, x2, y1, y2, z1, z2) = it
                .map(|s| s.unwrap().as_str().parse().unwrap())
                .collect_tuple()
                .unwrap();
            let min = Position::new(x1, y1, z1);
            let max = Position::new(x2, y2, z2);
            let cube = Cube::new(min, max);
            Action { cube, state }
        })
        .collect()
}

fn part_01(input: &Input) -> u64 {
    input
        .iter()
        .fold(HashSet::new(), |mut on_set, r| {
            for x in cmp::max(r.cube.min.x, -50)..=cmp::min(r.cube.max.x, 50) {
                for y in cmp::max(r.cube.min.y, -50)..=cmp::min(r.cube.max.y, 50) {
                    for z in cmp::max(r.cube.min.z, -50)..=cmp::min(r.cube.max.z, 50) {
                        if r.state {
                            on_set.insert(Position { x, y, z });
                        } else {
                            on_set.remove(&Position { x, y, z });
                        }
                    }
                }
            }
            return on_set;
        })
        .len() as u64
}

fn sum_volume(cubes: &Vec<Cube>) -> u64 {
    cubes.iter().map(|c| c.volume()).sum()
}

fn subtract_from_all(cubes: &Vec<Cube>, other: &Cube) -> Vec<Cube> {
    cubes.iter().flat_map(|c| c.subtract(&other)).collect()
}

fn part_02(input: &Input) -> u64 {
    let mut cubes = vec![];
    for action in input {
        cubes = subtract_from_all(&cubes, &action.cube);
        if action.state {
            cubes.push(action.cube);
        }
    }

    sum_volume(&cubes)
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_intersect_outside() {
        let a = Cube::new(Position::new(0, 0, 0), Position::new(1, 1, 1));
        let b = Cube::new(Position::new(2, 2, 2), Position::new(2, 2, 2));
        assert_eq!(a.intersect(&b), None);
        assert_eq!(b.intersect(&a), None);
    }

    #[test]
    fn test_intersect_contained() {
        let a = Cube::new(Position::new(0, 0, 0), Position::new(2, 3, 4));
        let b = Cube::new(Position::new(1, 2, 3), Position::new(1, 2, 3));
        assert_eq!(a.intersect(&b), Some(b));
        assert_eq!(b.intersect(&a), Some(b));
    }

    #[test]
    fn test_intersect_partial() {
        let a = Cube::new(Position::new(0, 0, 0), Position::new(2, 3, 4));
        let b = Cube::new(Position::new(-1, -2, -3), Position::new(1, 2, 3));
        let res = Cube::new(Position::new(0, 0, 0), Position::new(1, 2, 3));
        assert_eq!(a.intersect(&b), Some(res));
        assert_eq!(b.intersect(&a), Some(res));
    }

    #[test]
    fn test_subtract_no_overlap() {
        let a = Cube::new(Position::new(0, 0, 0), Position::new(5, 5, 5));
        let b = Cube::new(Position::new(7, 7, 7), Position::new(10, 10, 10));
        assert_eq!(a.subtract(&b), vec![a]);
    }

    #[test]
    fn test_subtract_larger() {
        let a = Cube::new(Position::new(1, 1, 1), Position::new(2, 2, 2));
        let b = Cube::new(Position::new(0, 0, 0), Position::new(3, 3, 3));
        assert_eq!(a.subtract(&b), vec![]);
    }

    #[test]
    fn test_subtract_inside() {
        let a = Cube::new(Position::new(0, 0, 0), Position::new(2, 2, 2));
        let b = Cube::new(Position::new(1, 1, 1), Position::new(1, 1, 1));
        assert_eq!(sum_volume(&a.subtract(&b)), a.volume() - 1);
    }

    #[test]
    fn test_subtract_corner() {
        let a = Cube::new(Position::new(0, 0, 0), Position::new(2, 2, 2));
        let b = Cube::new(Position::new(1, 1, 1), Position::new(3, 3, 3));
        let volume = a.volume() - a.intersect(&b).unwrap().volume();
        assert_eq!(sum_volume(&a.subtract(&b)), volume);
    }

    const EXAMPLE_DATA_1: &'static str = "
    on x=10..12,y=10..12,z=10..12
    on x=11..13,y=11..13,z=11..13
    off x=9..11,y=9..11,z=9..11
    on x=10..10,y=10..10,z=10..10
    ";

    const EXAMPLE_DATA_2: &'static str = include_str!("example2.txt");
    const EXAMPLE_DATA_3: &'static str = include_str!("example3.txt");

    #[test]
    fn example_1_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 39)
    }

    #[test]
    fn example_2_part_1() {
        let input = parse_input(EXAMPLE_DATA_2);
        assert_eq!(part_01(&input), 590784)
    }

    #[test]
    fn example_3_part_1() {
        let input = parse_input(EXAMPLE_DATA_3);
        assert_eq!(part_01(&input), 474140)
    }

    #[test]
    fn example_3_part_2() {
        let input = parse_input(EXAMPLE_DATA_3);
        assert_eq!(part_02(&input), 2758514936282235)
    }
}
