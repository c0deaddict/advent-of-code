use itertools::Itertools;
use lib::run;
use lib::astar::astar;
use std::collections::HashSet;

type Replacements<'a> = Vec<(&'a str, &'a str)>;

#[derive(Debug)]
struct Input<'a> {
    replacements: Replacements<'a>,
    molecule: &'a str,
}

fn parse_input(input: &str) -> Input {
    let (replacements, molecule) = input.trim().splitn(2, "\n\n").collect_tuple().unwrap();

    let replacements = replacements
        .lines()
        .map(|l| l.trim().splitn(2, " => ").collect_tuple().unwrap())
        .sorted_by_key(|(_, to)| to.len())
        .rev()
        .collect();

    let molecule = molecule.trim();

    Input {
        replacements,
        molecule,
    }
}

fn do_replacements<'a>(replacements: &Replacements<'a>, molecule: &'a str) -> HashSet<String> {
    let mut result = HashSet::new();
    for (from, to) in replacements {
        for (idx, _) in molecule.match_indices(from) {
            let mut new_molecule = molecule.to_string();
            new_molecule.replace_range(idx..idx + from.len(), to);
            result.insert(new_molecule);
        }
    }
    result
}

fn part_01(input: &Input) -> usize {
    do_replacements(&input.replacements, input.molecule).len()
}

fn adjacent<'a>(replacements: &Replacements<'a>, node: &'a str) -> Vec<(usize, String)> {
    do_replacements(replacements, node)
        .into_iter()
        .map(|next| (1 as usize, next))
        .collect()
}

fn part_02(input: &Input) -> usize {
    let reverse_replacements: Replacements = input.replacements
        .iter()
        .map(|(from, to)| (*to, *from))
        .collect();

    astar(
        &input.molecule,
        |n| adjacent(&reverse_replacements, &n),
        |n| n.len(),
        |n| *n == "e",
    ).len() - 1
}

fn main() {
    run(
        1,
        include_str!("../../../../input/day_19.txt"),
        parse_input,
        part_01,
        part_02,
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    H => HO
    H => OH
    O => HH

    HOHOHO
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 7)
    }

    const EXAMPLE_DATA_2: &'static str = "
    e => H
    e => O
    H => HO
    H => OH
    O => HH

    HOHOHO
    ";

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_2);
        assert_eq!(part_02(&input), 6)
    }
}
