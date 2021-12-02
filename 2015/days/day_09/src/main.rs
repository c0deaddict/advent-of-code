use std::collections::HashSet;

use lib::run;
use petgraph::{graphmap::UnGraphMap, visit::Dfs};
use regex::Regex;

type Input<'a> = UnGraphMap<&'a str, usize>;

fn parse_input(input: &str) -> Input {
    let re = Regex::new(r"^(.+) to (.+) = (\d+)$").unwrap();

    UnGraphMap::from_edges(
        input
            .lines()
            .map(|l| l.trim())
            .filter(|l| !l.is_empty())
            .map(|l| {
                let c = re.captures(l).unwrap();
                let from = c.get(1).unwrap().as_str();
                let to = c.get(2).unwrap().as_str();
                let dist: usize = c.get(3).unwrap().as_str().parse().unwrap();
                (from, to, dist)
            }),
    )
}

fn all_complete_paths(input: &Input) -> Vec<usize> {
    let mut distances = vec![];
    let unvisited: HashSet<_> = input.nodes().collect();
    let mut queue: Vec<(_, _, _)> = input.nodes().map(|n| (n, 0, unvisited.clone())).collect();
    while let Some((node, total_dist, mut unvisited)) = queue.pop() {
        unvisited.remove(node);
        if unvisited.is_empty() {
            distances.push(total_dist);
            continue;
        }

        for (_, next, dist) in input.edges(node) {
            if unvisited.contains(next) {
                queue.push((next, total_dist + dist, unvisited.clone()));
            }
        }
    }

    distances
}

fn part_01(input: &Input) -> usize {
    *all_complete_paths(input).iter().min().unwrap()
}

fn part_02(input: &Input) -> usize {
    *all_complete_paths(input).iter().max().unwrap()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    London to Dublin = 464
    London to Belfast = 518
    Dublin to Belfast = 141
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 605)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 982)
    }
}
