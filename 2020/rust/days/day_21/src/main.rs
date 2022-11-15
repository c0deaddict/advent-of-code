use itertools::Itertools;
use lib::run;
use std::collections::{HashMap, HashSet};

type Input<'a> = Vec<(Vec<&'a str>, Vec<&'a str>)>;

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .lines()
        .map(|line| {
            let parts: Vec<&str> = line.trim().splitn(2, " (contains ").collect();
            let ingredients = parts[0].trim().split(' ').collect();
            let allergens = parts[1].strip_suffix(')').unwrap().split(", ").collect();
            (ingredients, allergens)
        })
        .collect()
}

fn allergens_options<'a>(input: &'a Input) -> HashMap<&'a str, HashSet<&'a str>> {
    input
        .iter()
        .flat_map(|(ingredients, allergens)| {
            allergens
                .iter()
                .map(|name| {
                    (
                        *name,
                        ingredients.iter().cloned().collect::<HashSet<&'a str>>(),
                    )
                })
                .collect::<Vec<(&str, HashSet<&str>)>>()
        })
        .fold(HashMap::new(), |mut map, (k, v)| {
            map.entry(k)
                .and_modify(|old| *old = old.intersection(&v).cloned().collect())
                .or_insert(v);
            map
        })
}

fn find_allergens<'a>(input: &'a Input) -> HashMap<&'a str, &'a str> {
    let mut options = allergens_options(input);
    let mut mapping = HashMap::new();

    while !options.is_empty() {
        let alg = options
            .iter()
            .find_map(|(alg, ings)| {
                if ings.len() == 1 {
                    Some(alg.clone())
                } else {
                    None
                }
            })
            .unwrap();

        let (_, ings) = options.remove_entry(alg).unwrap();
        let ing = ings.iter().next().unwrap().clone();
        mapping.insert(alg, ing);

        options.iter_mut().for_each(|(_, ings)| {
            ings.remove(ing);
        });
    }

    mapping
}

fn part1(input: &Input) -> usize {
    let mapping = find_allergens(input);
    let mapped_ings: HashSet<_> = mapping.values().collect();

    input
        .iter()
        .flat_map(|(ings, _)| ings)
        .filter(|ing| !mapped_ings.contains(ing))
        .count()
}

fn part2(input: &Input) -> String {
    let mapping = find_allergens(input);
    mapping
        .iter()
        .sorted_by_key(|(alg, _)| *alg)
        .map(|(_, ing)| ing)
        .join(",")
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part1, part2)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
    trh fvjkl sbzzf mxmxvkd (contains dairy)
    sqjhc fvjkl (contains soy)
    sqjhc mxmxvkd sbzzf (contains fish)";

    #[test]
    fn example_1_part1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part1(&input), 5);
    }

    #[test]
    fn example_1_part2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part2(&input), "mxmxvkd,sqjhc,fvjkl");
    }
}
