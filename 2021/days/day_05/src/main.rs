use itertools::Itertools;
use lib::run;
use regex::Regex;
use std::cmp;
use std::collections::HashMap;

#[derive(Debug, Hash, Eq, PartialEq)]
struct Position {
    x: i32,
    y: i32,
}

#[derive(Debug)]
struct Line(Position, Position);

type Input = Vec<Line>;

fn parse_input(input: &str) -> Input {
    let re = Regex::new(r"(\d+),(\d+) -> (\d+),(\d+)$").unwrap();

    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| {
            let c = re.captures(l).unwrap();
            let (x1, y1, x2, y2) = c
                .iter()
                .skip(1)
                .map(|s| s.unwrap().as_str().parse().unwrap())
                .collect_tuple()
                .unwrap();
            Line(Position { x: x1, y: y1 }, Position { x: x2, y: y2 })
        })
        .collect()
}

fn part_01(input: &Input) -> usize {
    let mut map = HashMap::new();

    for line in input {
        let dx = line.1.x - line.0.x;
        let dy = line.1.y - line.0.y;

        if dx.abs() > 0 && dy.abs() > 0 {
            // Ignore diagonals.
            continue;
        }

        let len = cmp::max(dx.abs(), dy.abs());
        let dx = dx / len;
        let dy = dy / len;

        for i in 0..=len {
            let x = line.0.x + dx * i;
            let y = line.0.y + dy * i;
            map.entry(Position { x, y })
                .and_modify(|e| *e += 1)
                .or_insert(1);
        }
    }

    map.iter().filter(|(_, count)| **count >= 2).count()
}

fn part_02(input: &Input) -> usize {
    let mut map = HashMap::new();

    for line in input {
        let dx = line.1.x - line.0.x;
        let dy = line.1.y - line.0.y;
        let len = cmp::max(dx.abs(), dy.abs());
        let dx = dx / len;
        let dy = dy / len;

        for i in 0..=len {
            let x = line.0.x + dx * i;
            let y = line.0.y + dy * i;
            map.entry(Position { x, y })
                .and_modify(|e| *e += 1)
                .or_insert(1);
        }
    }

    map.iter().filter(|(_, count)| **count >= 2).count()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    0,9 -> 5,9
    8,0 -> 0,8
    9,4 -> 3,4
    2,2 -> 2,1
    7,0 -> 7,4
    6,4 -> 2,0
    0,9 -> 2,9
    3,4 -> 1,4
    0,0 -> 8,8
    5,5 -> 8,2
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 5)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 12)
    }
}
