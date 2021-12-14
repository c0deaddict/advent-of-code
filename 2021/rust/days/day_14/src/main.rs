use itertools::Itertools;
use lib::run;
use std::collections::HashMap;

type Rules<'a> = HashMap<&'a str, &'a str>;
type Pairs = HashMap<String, usize>;

#[derive(Debug)]
struct Input<'a> {
    template: &'a str,
    rules: Rules<'a>,
}

fn parse_input(input: &str) -> Input {
    let (template, rules) = input.trim().splitn(2, "\n\n").collect_tuple().unwrap();

    let rules = rules
        .trim()
        .lines()
        .map(|l| l.trim().splitn(2, " -> ").collect_tuple().unwrap())
        .collect();

    Input { template, rules }
}

fn step(polymer: &str, rules: &Rules) -> String {
    let mut out = polymer[0..=0].to_string();
    for i in 1..polymer.len() {
        if let Some(element) = rules.get(&polymer[i - 1..=i]) {
            out.push_str(element);
        }
        out.push_str(&polymer[i..=i]);
    }
    return out;
}

fn frequencies(polymer: &str) -> Vec<(char, usize)> {
    polymer
        .chars()
        .sorted()
        .group_by(|element| *element)
        .into_iter()
        .map(|(element, group)| (element, group.count()))
        .collect()
}

fn score(freqs: &Vec<(char, usize)>) -> usize {
    let most_common = freqs.iter().max_by_key(|(_, count)| count).unwrap().1;
    let least_common = freqs.iter().min_by_key(|(_, count)| count).unwrap().1;
    return most_common - least_common;
}

fn part_01(input: &Input) -> usize {
    let mut polymer = input.template.to_string();
    for _ in 0..10 {
        polymer = step(&polymer, &input.rules);
    }

    return score(&frequencies(&polymer));
}

fn get_pairs(polymer: &str) -> Pairs {
    let mut res = HashMap::new();
    for i in 1..polymer.len() {
        res.entry(polymer[i - 1..=i].to_string())
            .and_modify(|e| *e += 1)
            .or_insert(1);
    }
    return res;
}

fn step_with_pairs(pairs: &Pairs, rules: &Rules) -> Pairs {
    let mut res = HashMap::new();
    for (p, count) in pairs {
        if let Some(element) = rules.get(p.as_str()) {
            let p1 = p[0..=0].to_string() + element;
            let p2 = element.to_string() + &p[1..=1];
            res.entry(p1).and_modify(|e| *e += *count).or_insert(*count);
            res.entry(p2).and_modify(|e| *e += *count).or_insert(*count);
        } else {
            res.entry(p.to_string())
                .and_modify(|e| *e += 1)
                .or_insert(*count);
        }
    }
    return res;
}

fn first_and_last_char(s: &str) -> (char, char) {
    let mut it = s.chars();
    (it.next().unwrap(), it.last().unwrap())
}

fn part_02(input: &Input) -> usize {
    let mut pairs = get_pairs(input.template);
    for _ in 0..40 {
        pairs = step_with_pairs(&pairs, &input.rules);
    }

    let (first, last) = first_and_last_char(input.template);
    let freqs = pairs
        .iter()
        .fold(HashMap::new(), |mut acc, (p, count)| {
            let mut it = p.chars();
            acc.entry(it.next().unwrap())
                .and_modify(|e| *e += *count)
                .or_insert(*count);
            acc.entry(it.next().unwrap())
                .and_modify(|e| *e += *count)
                .or_insert(*count);
            return acc;
        })
        .into_iter()
        .map(|(ch, count)| {
            // Pairs are overlapping, so we have to divide to two.
            let count = if ch == first || ch == last {
                // The first and last char don't overlap, account for that.
                (count + 1) / 2
            } else {
                count / 2
            };
            (ch, count)
        })
        .collect();

    return score(&freqs);
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    NNCB

    CH -> B
    HH -> N
    CB -> H
    NH -> C
    HB -> C
    HC -> B
    HN -> C
    NN -> C
    BH -> H
    NC -> B
    NB -> B
    BN -> B
    BB -> N
    BC -> B
    CC -> N
    CN -> C
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 1588)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 2188189693529)
    }
}
