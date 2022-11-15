use itertools::Itertools;
use lib::run;
use regex::Regex;
use std::collections::HashMap;
use std::fmt::Debug;

#[derive(Debug)]
struct PasswordEntry {
    i: usize,
    j: usize,
    ch: char,
    password: String,
}

type Input = Vec<PasswordEntry>;

fn parse_input(input: &str) -> Input {
    let re = Regex::new(r"^(\d+)-(\d+) ([a-z]): ([a-z]+)$").unwrap();

    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| re.captures(l).unwrap())
        .map(|c| PasswordEntry {
            i: c[1].parse::<usize>().unwrap(),
            j: c[2].parse::<usize>().unwrap(),
            ch: c[3].chars().next().unwrap(),
            password: c[4].to_owned(),
        })
        .collect()
}

fn frequencies(s: &str) -> HashMap<char, usize> {
    s.chars()
        .sorted()
        .group_by(|c| c.to_owned())
        .into_iter()
        .map(|(c, g)| (c, g.count()))
        .collect()
}

fn is_valid_part1(entry: &PasswordEntry) -> bool {
    let f = frequencies(&entry.password);
    let reps = *f.get(&entry.ch).unwrap_or(&0);
    reps >= entry.i && reps <= entry.j
}

fn part_01(input: &Input) -> usize {
    input.iter().filter(|e| is_valid_part1(e)).count()
}

fn is_valid_part2(entry: &PasswordEntry) -> bool {
    let chars: Vec<char> = entry.password.chars().collect();
    let a = chars[entry.i - 1] == entry.ch;
    let b = chars[entry.j - 1] == entry.ch;
    (a || b) && !(a && b)
}

fn part_02(input: &Input) -> usize {
    input.iter().filter(|e| is_valid_part2(e)).count()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    1-3 a: abcde
    1-3 b: cdefg
    2-9 c: ccccccccc";

    #[test]
    fn test_frequencies() {
        let freq = frequencies("ababbba");
        assert_eq!(*freq.get(&'a').unwrap(), 3);
        assert_eq!(*freq.get(&'b').unwrap(), 4);
    }

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 2)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 1);
    }
}
