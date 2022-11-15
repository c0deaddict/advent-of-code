use itertools::Itertools;
use lib::run;
use std::collections::{HashMap, HashSet};

type Input<'r> = HashMap<&'r str, Vec<(usize, &'r str)>>;
type ContainsGraph<'r> = HashMap<&'r str, Vec<(usize, &'r str)>>;

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .lines()
        .map(|l| {
            let (bag, rest) = l.splitn(2, " bags contain ").collect_tuple().unwrap();
            let contains = if rest == "no other bags." {
                vec![]
            } else {
                rest.split(", ")
                    .map(|b| {
                        let (count, rest) = b.splitn(2, " ").collect_tuple().unwrap();
                        let (bag, _) = rest.splitn(2, " bag").collect_tuple().unwrap();
                        (count.parse::<usize>().unwrap(), bag)
                    })
                    .collect()
            };
            (bag.trim(), contains)
        })
        .collect()
}

fn build_contains_graph<'r>(input: &'r Input) -> ContainsGraph<'r> {
    let it = input.iter().flat_map(move |(parent, children)| {
        children
            .iter()
            .map(move |(count, child)| (*child, (*count, *parent)))
    });

    let mut graph: ContainsGraph = HashMap::new();
    for (child, (count, parent)) in it {
        graph
            .entry(child)
            .and_modify(|v| v.push((count, parent)))
            .or_insert(vec![(count, parent)]);
    }

    graph
}

fn part_01(input: &Input) -> usize {
    let graph = build_contains_graph(input);
    let mut visited: HashSet<&str> = HashSet::new();
    let mut parent_count = 0;
    let mut queue = vec!["shiny gold"];
    while !queue.is_empty() {
        let bag = queue.pop().unwrap();
        if let Some(parents) = graph.get(bag) {
            for (_count, parent) in parents {
                if visited.insert(parent) {
                    queue.push(parent);
                    parent_count += 1;
                }
            }
        }
    }
    parent_count
}

fn count_bags(bag: &str, input: &Input) -> usize {
    1 + input
        .get(bag)
        .map(|children| {
            children
                .iter()
                .map(|(count, child)| count * count_bags(child, input))
                .sum()
        })
        .unwrap_or(0)
}

fn part_02(input: &Input) -> usize {
    count_bags("shiny gold", input) - 1
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    light red bags contain 1 bright white bag, 2 muted yellow bags.
    dark orange bags contain 3 bright white bags, 4 muted yellow bags.
    bright white bags contain 1 shiny gold bag.
    muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
    shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
    dark olive bags contain 3 faded blue bags, 4 dotted black bags.
    vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
    faded blue bags contain no other bags.
    dotted black bags contain no other bags.";

    const EXAMPLE_DATA_2: &'static str = "
    shiny gold bags contain 2 dark red bags.
    dark red bags contain 2 dark orange bags.
    dark orange bags contain 2 dark yellow bags.
    dark yellow bags contain 2 dark green bags.
    dark green bags contain 2 dark blue bags.
    dark blue bags contain 2 dark violet bags.
    dark violet bags contain no other bags.";

    #[test]
    fn test_parse_input() {
        let input = parse_input(EXAMPLE_DATA_1);
        println!("{:?}", input);
        assert_eq!(
            input.get("bright white").unwrap(),
            &vec![(1 as usize, "shiny gold")]
        );
    }

    #[test]
    fn test_contains_graph() {
        let input = parse_input(EXAMPLE_DATA_1);
        let contains_graph = build_contains_graph(&input);
        assert_eq!(
            contains_graph
                .get("dark olive")
                .unwrap()
                .contains(&(1 as usize, "shiny gold")),
            true
        );
        assert_eq!(
            contains_graph
                .get("muted yellow")
                .unwrap()
                .contains(&(2 as usize, "light red")),
            true
        );
        assert_eq!(
            contains_graph
                .get("muted yellow")
                .unwrap()
                .contains(&(4 as usize, "dark orange")),
            true
        );
    }

    #[test]
    fn example_part_01() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 4);
    }

    #[test]
    fn example1_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 32);
    }

    #[test]
    fn example2_part_2() {
        let input = parse_input(EXAMPLE_DATA_2);
        assert_eq!(part_02(&input), 126);
    }
}
