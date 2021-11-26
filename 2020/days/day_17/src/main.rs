use lib::run;
use std::clone::Clone;
use std::cmp::{Eq, PartialEq};
use std::collections::HashSet;
use std::fmt::Debug;
use std::hash::Hash;
use std::marker::Copy;

#[derive(PartialEq, Eq, Hash, Debug, Clone, Copy)]
struct Point {
    x: i64,
    y: i64,
    z: i64,
    w: i64,
}

impl Point {
    fn new(x: i64, y: i64, z: i64, w: i64) -> Point {
        Point { x, y, z, w }
    }

    fn neighbours(&self, four_d: bool) -> Vec<Point> {
        if four_d {
            self.neighbours_4d()
        } else {
            self.neighbours_3d()
        }
    }

    fn neighbours_3d(&self) -> Vec<Point> {
        let mut result = vec![];
        for x in (self.x - 1)..(self.x + 2) {
            for y in (self.y - 1)..(self.y + 2) {
                for z in (self.z - 1)..(self.z + 2) {
                    if x != self.x || y != self.y || z != self.z {
                        result.push(Point::new(x, y, z, self.w));
                    }
                }
            }
        }

        result
    }

    fn neighbours_4d(&self) -> Vec<Point> {
        let mut result = vec![];
        for x in (self.x - 1)..(self.x + 2) {
            for y in (self.y - 1)..(self.y + 2) {
                for z in (self.z - 1)..(self.z + 2) {
                    for w in (self.w - 1)..(self.w + 2) {
                        if x != self.x || y != self.y || z != self.z || w != self.w {
                            result.push(Point::new(x, y, z, w));
                        }
                    }
                }
            }
        }

        result
    }
}

type Input = HashSet<Point>;

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .lines()
        .enumerate()
        .flat_map(move |(y, line)| {
            line.trim()
                .chars()
                .enumerate()
                .filter_map(move |(x, state)| {
                    if state == '#' {
                        Some(Point::new(x as i64, y as i64, 0, 0))
                    } else {
                        None
                    }
                })
        })
        .collect()
}

fn conway_step(input: &Input, four_d: bool) -> Input {
    let mut result: Input = HashSet::new();
    let mut inactive_field: Input = HashSet::new();

    for p in input {
        let mut active_count = 0;
        for n in p.neighbours(four_d) {
            if input.contains(&n) {
                active_count += 1;
            } else {
                inactive_field.insert(n);
            }
        }

        if active_count == 2 || active_count == 3 {
            result.insert(*p);
        }
    }

    for p in inactive_field {
        let mut active_count = 0;
        for n in p.neighbours(four_d) {
            if input.contains(&n) {
                active_count += 1;
            }
        }

        if active_count == 3 {
            result.insert(p);
        }
    }

    result
}

fn conway(input: &Input, cycles: usize, four_d: bool) -> usize {
    if cycles == 0 {
        input.len()
    } else {
        conway(&conway_step(input, four_d), cycles - 1, four_d)
    }
}

fn part1(input: &Input) -> usize {
    conway(input, 6, false)
}

fn part2(input: &Input) -> usize {
    conway(input, 6, true)
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part1, part2)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    .#.
    ..#
    ###";

    #[test]
    fn test_parse_input() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(input.len(), 5);
    }

    #[test]
    fn example_1_part1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part1(&input), 112);
    }

    #[test]
    fn example_1_part2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part2(&input), 848);
    }
}
