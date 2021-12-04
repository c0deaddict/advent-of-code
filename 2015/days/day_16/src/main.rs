use itertools::Itertools;
use lazy_static::lazy_static;
use lib::run;
use std::collections::HashMap;

type Input<'a> = Vec<(usize, HashMap<&'a str, usize>)>;

fn parse_input(input: &str) -> Input {
    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| {
            let (name, properties) = l.splitn(2, ": ").collect_tuple().unwrap();
            let id = name[4..].parse().unwrap();
            let map = properties
                .split(", ")
                .map(|kv| {
                    let (key, value) = kv.splitn(2, ": ").collect_tuple().unwrap();
                    (key, value.parse().unwrap())
                })
                .collect();
            (id, map)
        })
        .collect()
}

lazy_static! {
    static ref PROPERTIES: HashMap<&'static str, usize> = HashMap::from([
        ("children", 3),
        ("cats", 7),
        ("samoyeds", 2),
        ("pomeranians", 3),
        ("akitas", 0),
        ("vizslas", 0),
        ("goldfish", 5),
        ("trees", 3),
        ("cars", 2),
        ("perfumes", 1),
    ]);
}

fn part_01(input: &Input) -> usize {
    let mut candidates = input.clone();
    for (key, value) in PROPERTIES.iter() {
        candidates.retain(|(_, p)| match p.get(key) {
            None => true,
            Some(v) => v == value,
        });
    }

    if candidates.len() != 1 {
        panic!("expected one aunt to be left");
    }

    candidates[0].0
}

fn part_02(input: &Input) -> usize {
    let mut candidates = input.clone();
    for (key, value) in PROPERTIES.iter() {
        candidates.retain(|(_, p)| match p.get(key) {
            None => true,
            Some(v) => match *key {
                "cats" | "trees" => v > value,
                "pomeranians" | "goldfish" => v < value,
                _ => v == value,
            },
        });
    }

    if candidates.len() != 1 {
        panic!("expected one aunt to be left");
    }

    candidates[0].0
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;
}
