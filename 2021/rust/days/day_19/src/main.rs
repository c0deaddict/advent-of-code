use itertools::Itertools;
use lazy_static::lazy_static;
use lib::run;
use regex::Regex;
use std::collections::{HashMap, HashSet};

use Axis::*;

#[derive(Debug, Hash, Eq, PartialEq, Copy, Clone, Ord, PartialOrd)]
struct Vector {
    x: i32,
    y: i32,
    z: i32,
}

#[derive(Debug, Clone)]
enum Axis {
    X,
    Y,
}

#[derive(Debug, Clone)]
struct Rotation(Vec<Axis>, Vec<Axis>);

lazy_static! {
    // Note: Should have used matrices..
    // https://www.euclideanspace.com/maths/discrete/groups/categorise/finite/cube/index.htm
    static ref ROTATIONS: Vec<Rotation> = vec![
        Rotation(vec![], vec![]),
        Rotation(vec![X], vec![X, X, X]),
        Rotation(vec![Y], vec![Y, Y, Y]),
        Rotation(vec![X, X], vec![X, X]),
        Rotation(vec![X, Y], vec![X, X, Y, X]),
        Rotation(vec![Y, X], vec![X, Y, X, X]),
        Rotation(vec![Y, Y], vec![Y, Y]),
        Rotation(vec![X, X, X], vec![X]),
        Rotation(vec![X, X, Y], vec![X, X, Y]),
        Rotation(vec![X, Y, X], vec![X, Y, X]),
        Rotation(vec![X, Y, Y], vec![X, Y, Y]),
        Rotation(vec![Y, X, X], vec![Y, X, X]),
        Rotation(vec![Y, Y, X], vec![Y, Y, X]),
        Rotation(vec![Y, Y, Y], vec![Y]),
        Rotation(vec![X, X, X, Y], vec![Y, Y, Y, X]),
        Rotation(vec![X, X, Y, X], vec![X, Y]),
        Rotation(vec![X, X, Y, Y], vec![X, X, Y, Y]),
        Rotation(vec![X, Y, X, X], vec![Y, X]),
        Rotation(vec![X, Y, Y, Y], vec![Y, X, X, X]),
        Rotation(vec![Y, X, X, X], vec![X, Y, Y, Y]),
        Rotation(vec![Y, Y, Y, X], vec![X, X, X, Y]),
        Rotation(vec![X, X, X, Y, X], vec![X, Y, X, X, X]),
        Rotation(vec![X, Y, X, X, X], vec![X, X, X, Y, X]),
        Rotation(vec![X, Y, Y, Y, X], vec![X, Y, Y, Y, X]),
    ];
}

impl Vector {
    fn new(x: i32, y: i32, z: i32) -> Vector {
        Vector{x, y, z}
    }

    fn rotate(&self, r: &Rotation) -> Vector {
        r.0.iter().fold(self.clone(), |p, axis| match axis {
            X => Vector {
                x: p.x,
                y: -p.z,
                z: p.y,
            },
            Y => Vector {
                x: p.z,
                y: p.y,
                z: -p.x,
            },
        })
    }

    fn add(&self, o: &Vector) -> Vector {
        Vector {
            x: self.x + o.x,
            y: self.y + o.y,
            z: self.z + o.z,
        }
    }

    fn subtract(&self, o: &Vector) -> Vector {
        Vector {
            x: self.x - o.x,
            y: self.y - o.y,
            z: self.z - o.z,
        }
    }

    fn abs(&self) -> Vector {
        Vector {
            x: self.x.abs(),
            y: self.y.abs(),
            z: self.z.abs(),
        }
    }

    fn sqr_len(&self) -> i32 {
        self.x * self.x + self.y * self.y + self.z * self.z
    }

    fn apply_transforms(&self, transforms: &Vec<(Rotation, Vector)>) -> Vector {
        let mut res = self.clone();
        for (rot, offset) in transforms.iter().rev() {
            res = res.rotate(&rot).add(&offset);
        }
        return res;
    }

    fn manhattan(&self) -> i32 {
        self.x + self.y + self.z
    }
}

type Input = Vec<Vec<Vector>>;

fn parse_input(input: &str) -> Input {
    let header_re = Regex::new(r"^--- scanner (\d+) ---$").unwrap();
    input
        .trim()
        .split("\n\n")
        .enumerate()
        .map(|(id, chunk)| {
            let mut lines = chunk.trim().lines();
            let header = lines.next().unwrap();
            let header_id: usize = header_re
                .captures(header)
                .unwrap()
                .get(1)
                .unwrap()
                .as_str()
                .parse()
                .unwrap();
            if header_id != id {
                panic!("scanners not in order, expected {} got {}", id, header_id);
            }

            lines
                .map(|l| {
                    let (x, y, z) = l
                        .trim()
                        .split(",")
                        .map(|s| s.parse().unwrap())
                        .collect_tuple()
                        .unwrap();
                    Vector { x, y, z }
                })
                .collect()
        })
        .collect()
}

/// Search for beacons that have the same relative distance in s0 and s1.
fn possible_common_beacons(
    s0: &Vec<Vector>,
    s1: &Vec<Vector>,
) -> Option<(Vec<Vector>, Vec<Vector>)> {
    let mut distances = HashMap::<i32, Vec<(&Vector, &Vector)>>::new();
    for v in s0.iter().combinations(2) {
        distances
            .entry(v[0].subtract(v[1]).abs().sqr_len())
            .and_modify(|e| e.push((v[0], v[1])))
            .or_insert(vec![(v[0], v[1])]);
    }

    let mut left = HashSet::new();
    let mut right = HashSet::new();

    for v in s1.iter().combinations(2) {
        distances
            .entry(v[0].subtract(v[1]).abs().sqr_len())
            .and_modify(|e| {
                if let Some((a, b)) = e.pop() {
                    left.insert(*a);
                    left.insert(*b);
                    right.insert(*v[0]);
                    right.insert(*v[1]);
                }
            });
    }

    if left.len() >= 12 && right.len() >= 12 {
        Some((
            left.iter().cloned().collect(),
            right.iter().cloned().collect(),
        ))
    } else {
        None
    }
}

/// Find orientation of p2 compared to p1.
fn find_rotation(p1: &Vec<Vector>, p2: &Vec<Vector>) -> Option<&'static Rotation> {
    let d1: HashMap<_, _> = p1
        .iter()
        .combinations(2)
        .flat_map(|v| {
            vec![
                ((v[0], v[1]), v[0].subtract(v[1])),
                ((v[1], v[0]), v[1].subtract(v[0])),
            ]
        })
        .collect();

    ROTATIONS.iter().find(|r| {
        p2.iter()
            .map(|v| v.rotate(r))
            .combinations(2)
            .filter(|v| {
                d1.values().contains(&v[0].subtract(&v[1]))
                    || d1.values().contains(&v[1].subtract(&v[0]))
            })
            .count()
            >= 66 // (12 over 2)
    })
}

/// Find offset of p2 relative to p1.
fn find_offset(p1: &Vec<Vector>, p2: &Vec<Vector>) -> Option<Vector> {
    p1.iter().cartesian_product(p2.iter()).find_map(|(a, b)| {
        let offset = a.subtract(b);
        if p2.iter().filter(|p| p1.contains(&p.add(&offset))).count() >= 12 {
            Some(offset)
        } else {
            None
        }
    })
}

fn map_scanners_and_beacons(input: &Input) -> (HashMap<usize, Vector>, HashSet<Vector>) {
    let edges = input
        .iter()
        .enumerate()
        .permutations(2)
        .filter_map(|pair| {
            // For each combination of scanners, try to find a minimal shared beacon
            // set (>= 12).
            possible_common_beacons(&pair[0].1, &pair[1].1)
                .and_then(|(a, b)| {
                    // Find the rotation of b so that it aligns to a.
                    find_rotation(&a, &b).map(|rot| {
                        // Rotate b to align to a.
                        (rot, a, b.iter().map(|p| p.rotate(rot)).collect())
                    })
                })
                .and_then(|(rot, a, b)| {
                    // Try to find an offset that matches all shared points between a and b.
                    find_offset(&a, &b).map(|offset| ((pair[0].0, pair[1].0), (rot, offset)))
                })
        })
        .fold(HashMap::new(), |mut map, ((from, to), (rot, offset))| {
            map.insert((from, to), (rot.clone(), offset));
            map
        });

    let mut scanners = HashMap::new();
    scanners.insert(0, Vector::new(0, 0, 0));
    let mut beacons = HashSet::new();
    let mut queue = vec![(0, vec![])];
    while let Some((i, transforms)) = queue.pop() {
        // Apply transforms to all points from scanner and add them to beacons.
        beacons.extend(input[i].iter().map(|v| v.apply_transforms(&transforms)));

        // Find an edge from scanner to any next point.
        for ((from, to), next_transform) in &edges {
            if *from == i && !scanners.contains_key(to) {
                let mut transforms = transforms.clone();
                transforms.push(next_transform.clone());
                let center = Vector::new(0, 0, 0).apply_transforms(&transforms);
                scanners.insert(*to, center);
                queue.push((*to, transforms));
            }
        }
    }

    return (scanners, beacons);
}

fn part_01(input: &Input) -> usize {
    let (_, beacons)  = map_scanners_and_beacons(&input);
    return beacons.len();
}

fn part_02(input: &Input) -> i32 {
    let (scanners, _)  = map_scanners_and_beacons(&input);
    scanners.values().combinations(2).map(|v| {
        v[0].subtract(v[1]).abs().manhattan()
    }).max().unwrap()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = include_str!("example.txt");

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 79)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 3621)
    }    
}
