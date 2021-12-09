use itertools::Itertools;
use lib::run;
use std::collections::{HashMap, HashSet};

#[derive(Debug, Hash, Eq, PartialEq, Copy, Clone)]
struct Position {
    x: i32,
    y: i32,
}

type Input = HashMap<Position, usize>;

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .lines()
        .enumerate()
        .flat_map(|(y, l)| {
            l.trim()
                .chars()
                .enumerate()
                .map(|(x, h)| {
                    let x = x as i32;
                    let y = y as i32;
                    (Position { x, y }, h.to_string().parse().unwrap())
                })
                .collect::<Vec<_>>()
        })
        .collect()
}

fn neighbours(pos: &Position) -> Vec<Position> {
    vec![
        Position {
            x: pos.x - 1,
            y: pos.y,
        },
        Position {
            x: pos.x + 1,
            y: pos.y,
        },
        Position {
            x: pos.x,
            y: pos.y - 1,
        },
        Position {
            x: pos.x,
            y: pos.y + 1,
        },
    ]
}

fn low_points(input: &Input) -> Vec<(Position, usize)> {
    input
        .iter()
        .filter(|(pos, height)| {
            neighbours(pos)
                .iter()
                .all(|n| input.get(n).map(|h| h > height).unwrap_or(true))
        })
        .map(|(pos, height)| (*pos, *height))
        .collect()
}

fn part_01(input: &Input) -> usize {
    low_points(input).iter().map(|(_, height)| height + 1).sum()
}

fn discover_basin(input: &Input, start: Position) -> HashSet<Position> {
    let mut basin = HashSet::new();
    let mut queue = vec![start];
    while let Some(pos) = queue.pop() {
        if input.get(&pos).map(|h| *h == 9).unwrap_or(true) {
            // At the edge.
            continue;
        }

        // Part of basin.
        basin.insert(pos);

        for n in neighbours(&pos) {
            if !basin.contains(&n) {
                queue.push(n);
            }
        }
    }

    return basin;
}

fn part_02(input: &Input) -> usize {
    let mut all_basins = HashSet::new();
    low_points(input)
        .iter()
        .filter_map(|(pos, _)| {
            // Check that the low point if not part of an already discovered basin.
            if all_basins.contains(pos) {
                None
            } else {
                let basin = discover_basin(input, pos.clone());
                let size = basin.len();
                all_basins.extend(basin);
                Some(size)
            }
        })
        .sorted()
        .rev()
        .take(3)
        .reduce(|a, b| a * b)
        .unwrap()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    2199943210
    3987894921
    9856789892
    8767896789
    9899965678
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 15)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 1134)
    }
}
