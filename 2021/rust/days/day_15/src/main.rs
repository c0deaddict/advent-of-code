use itertools::Itertools;
use lib::run;
use petgraph::{algo::dijkstra, graphmap::DiGraphMap};
use std::collections::HashMap;

#[derive(Debug, Hash, Eq, PartialEq, Copy, Clone, Ord, PartialOrd)]
struct Position {
    x: i32,
    y: i32,
}

type Input = HashMap<Position, usize>;

fn neighbours(pos: &Position) -> Vec<Position> {
    [(-1, 0), (0, -1), (1, 0), (0, 1)]
        .iter()
        .map(|(x, y)| Position {
            x: pos.x + x,
            y: pos.y + y,
        })
        .collect()
}

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .lines()
        .enumerate()
        .flat_map(|(y, l)| {
            l.trim()
                .chars()
                .enumerate()
                .map(|(x, risk)| {
                    let x = x as i32;
                    let y = y as i32;
                    (Position { x, y }, risk.to_string().parse().unwrap())
                })
                .collect::<Vec<_>>()
        })
        .collect()
}

fn shortest_path(input: &Input) -> usize {
    let maxx = input.keys().max_by_key(|p| p.x).unwrap().x;
    let maxy = input.keys().max_by_key(|p| p.y).unwrap().y;
    let from = Position { x: 0, y: 0 };
    let to = Position { x: maxx, y: maxy };

    let graph = DiGraphMap::from_edges(input.keys().flat_map(|from| {
        neighbours(from)
            .iter()
            .filter_map(|to| input.get(to).map(|risk| (*from, *to, *risk)))
            .collect::<Vec<_>>()
    }));

    *dijkstra(&graph, from, Some(to), |e| *e.2).get(&to).unwrap()
}

fn part_01(input: &Input) -> usize {
    shortest_path(&input)
}

fn extend_map(input: &Input) -> Input {
    let width = input.keys().max_by_key(|p| p.x).unwrap().x + 1;
    let height = input.keys().max_by_key(|p| p.y).unwrap().y + 1;

    (0..5)
        .cartesian_product(0..5)
        .cartesian_product(input.iter())
        .map(|((rx, ry), (pos, risk))| {
            let x = pos.x + rx * width;
            let y = pos.y + ry * height;
            let risk = 1 + ((risk + ((rx + ry) as usize) - 1) % 9);
            (Position { x, y }, risk)
        })
        .collect()
}

fn part_02(input: &Input) -> usize {
    shortest_path(&extend_map(&input))
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    1163751742
    1381373672
    2136511328
    3694931569
    7463417111
    1319128137
    1359912421
    3125421639
    1293138521
    2311944581
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 40)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 315)
    }
}
