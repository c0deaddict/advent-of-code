use std::collections::HashMap;

use lib::run;

type Input<'a> = Vec<&'a str>;

fn parse_input(input: &str) -> Input {
    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .collect()
}

const VOWELS: &'static str = "aeiou";
const FORBIDDEN: &'static [&str] = &["ab", "cd", "pq", "xy"];

fn is_nice_string(s: &str) -> bool {
    let mut vowel_count = 0;
    let mut double = false;
    let mut prev: Option<char> = None;

    for ch in s.chars() {
        if VOWELS.contains(ch) {
            vowel_count += 1;
        }

        if let Some(prev_ch) = prev {
            if ch == prev_ch {
                double = true;
            }

            if FORBIDDEN.contains(&format!("{}{}", prev_ch, ch).as_str()) {
                return false;
            }
        }

        prev = Some(ch);
    }

    vowel_count >= 3 && double
}

fn part_01(input: &Input) -> usize {
    input.iter().filter(|s| is_nice_string(s)).count()
}

fn is_nice_part2(s: &str) -> bool {
    // Search for xyx pattern.
    let mut found = false;
    for i in 2..s.len() {
        if s[i - 2..i - 1] == s[i..i + 1] {
            found = true;
            break;
        }
    }
    if !found {
        return false;
    }

    // Index all pairs.
    let mut pairs: HashMap<&str, Vec<usize>> = HashMap::new();
    for i in 1..s.len() {
        pairs
            .entry(&s[i - 1..i + 1])
            .and_modify(|e| e.push(i - 1))
            .or_insert(vec![i - 1]);
    }

    // Search for identical pairs not sharing any characters.
    pairs
        .iter()
        .find(|(_, positions)| {
            let min = positions.iter().min().unwrap();
            let max = positions.iter().max().unwrap();
            return max - min >= 2;
        })
        .is_some()
}

fn part_02(input: &Input) -> usize {
    input.iter().filter(|s| is_nice_part2(s)).count()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn examples_part_1() {
        assert_eq!(is_nice_string("ugknbfddgicrmopn"), true);
        assert_eq!(is_nice_string("aaa"), true);
        assert_eq!(is_nice_string("jchzalrnumimnmhp"), false);
        assert_eq!(is_nice_string("haegwjzuvuyypxyu"), false);
        assert_eq!(is_nice_string("dvszwmarrgswjxmb"), false);
    }

    #[test]
    fn examples_part_2() {
        assert_eq!(is_nice_part2("qjhvhtzxzqqjkmpb"), true);
        assert_eq!(is_nice_part2("xxyxx"), true);
        assert_eq!(is_nice_part2("uurcxstgmygtbstg"), false);
        assert_eq!(is_nice_part2("ieodomkazucvgmuy"), false);
        assert_eq!(is_nice_part2("aaa"), false);
    }
}
