use itertools::Itertools;
use lib::run;
use regex::Regex;
use std::collections::{HashMap, HashSet};

type Input<'a> = HashMap<(&'a str, &'a str), i32>;

fn parse_input(input: &str) -> Input {
    let re =
        Regex::new(r"^(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+).$")
            .unwrap();

    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| {
            let c = re.captures(l).unwrap();
            let from = c.get(1).unwrap().as_str();
            let to = c.get(4).unwrap().as_str();
            let mut weight: i32 = c.get(3).unwrap().as_str().parse().unwrap();
            if c.get(2).unwrap().as_str() == "lose" {
                weight = -weight;
            }
            ((from, to), weight)
        })
        .collect()
}

fn get_people<'a>(input: &'a Input) -> HashSet<&'a str> {
    let mut people = HashSet::new();
    for ((from, to), _) in input {
        people.insert(*from);
        people.insert(*to);
    }
    people
}

fn compute_happiness<'a>(order: &Vec<&'a str>, edges: &'a Input) -> i32 {
    let mut happiness = 0;
    for (i, name) in order.iter().enumerate() {
        let right = order[(i + 1) % order.len()];
        happiness += edges.get(&(name, right)).unwrap();
        happiness += edges.get(&(right, name)).unwrap();
    }
    happiness
}

fn maximum_happiness<'a>(people: HashSet<&'a str>, edges: &'a Input) -> i32 {
    let count = people.len();
    people
        .into_iter()
        .permutations(count)
        .map(|order| compute_happiness(&order, edges))
        .max()
        .unwrap()
}

fn part_01(input: &Input) -> i32 {
    maximum_happiness(get_people(input), input)
}

fn part_02(input: &Input) -> i32 {
    let me = "Me, myself and I";
    let mut people = get_people(input);
    let mut edges = input.clone();
    for other in &people {
        edges.insert((me, other), 0);
        edges.insert((other, me), 0);
    }
    people.insert(me);

    maximum_happiness(people, &edges)
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    Alice would gain 54 happiness units by sitting next to Bob.
    Alice would lose 79 happiness units by sitting next to Carol.
    Alice would lose 2 happiness units by sitting next to David.
    Bob would gain 83 happiness units by sitting next to Alice.
    Bob would lose 7 happiness units by sitting next to Carol.
    Bob would lose 63 happiness units by sitting next to David.
    Carol would lose 62 happiness units by sitting next to Alice.
    Carol would gain 60 happiness units by sitting next to Bob.
    Carol would gain 55 happiness units by sitting next to David.
    David would gain 46 happiness units by sitting next to Alice.
    David would lose 7 happiness units by sitting next to Bob.
    David would gain 41 happiness units by sitting next to Carol.
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 330)
    }
}
