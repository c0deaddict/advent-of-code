use itertools::Itertools;
use lib::run;
use std::collections::{HashMap, HashSet};

type Input<'a> = HashMap<&'a str, Vec<&'a str>>;

fn parse_input(input: &str) -> Input {
    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| l.splitn(2, "-").collect_tuple().unwrap())
        .fold(HashMap::new(), |mut edges, (from, to)| {
            edges
                .entry(from)
                .and_modify(|e| e.push(to))
                .or_insert(vec![to]);
            edges
                .entry(to)
                .and_modify(|e| e.push(from))
                .or_insert(vec![from]);
            return edges;
        })
}

fn is_big_cave(v: &str) -> bool {
    v.chars().next().unwrap().is_uppercase()
}

fn count_all_paths(edges: &Input, node: &str, visited: &HashSet<&str>) -> usize {
    let mut visited = visited.clone();
    visited.insert(node);

    if node == "end" {
        return 1;
    } else if let Some(neighbours) = edges.get(node) {
        let mut count = 0;
        for n in neighbours {
            if is_big_cave(n) || !visited.contains(n) {
                count += count_all_paths(edges, n, &visited);
            }
        }
        return count;
    } else {
        return 0;
    }
}

fn part_01(input: &Input) -> usize {
    count_all_paths(input, "start", &HashSet::new())
}

fn count_visit_twice_paths(edges: &Input, node: &str, visited: &HashSet<&str>) -> usize {
    let mut visited = visited.clone();
    visited.insert(node);

    if node == "end" {
        return 0;
    } else if let Some(neighbours) = edges.get(node) {
        let mut count = 0;
        for n in neighbours {
            if is_big_cave(n) || !visited.contains(n) {
                count += count_visit_twice_paths(edges, n, &visited);
            } else if *n != "start" {
                count += count_all_paths(edges, n, &visited);
            }
        }
        return count;
    } else {
        return 0;
    }
}

fn part_02(input: &Input) -> usize {
    count_all_paths(input, "start", &HashSet::new())
        + count_visit_twice_paths(input, "start", &HashSet::new())
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    start-A
    start-b
    A-c
    A-b
    b-d
    A-end
    b-end
    ";

    const EXAMPLE_DATA_2: &'static str = "
    dc-end
    HN-start
    start-kj
    dc-start
    dc-HN
    LN-dc
    HN-end
    kj-sa
    kj-HN
    kj-dc
    ";

    const EXAMPLE_DATA_3: &'static str = "
    fs-end
    he-DX
    fs-he
    start-DX
    pj-DX
    end-zg
    zg-sl
    zg-pj
    pj-he
    RW-he
    fs-DX
    pj-RW
    zg-RW
    start-pj
    he-WI
    zg-he
    pj-fs
    start-RW
    ";

    #[test]
    fn example_1_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 10)
    }

    #[test]
    fn example_2_part_1() {
        let input = parse_input(EXAMPLE_DATA_2);
        assert_eq!(part_01(&input), 19)
    }

    #[test]
    fn example_3_part_1() {
        let input = parse_input(EXAMPLE_DATA_3);
        assert_eq!(part_01(&input), 226)
    }

    #[test]
    fn example_1_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 36)
    }

    #[test]
    fn example_2_part_2() {
        let input = parse_input(EXAMPLE_DATA_2);
        assert_eq!(part_02(&input), 103)
    }

    #[test]
    fn example_3_part_2() {
        let input = parse_input(EXAMPLE_DATA_3);
        assert_eq!(part_02(&input), 3509)
    }
}
