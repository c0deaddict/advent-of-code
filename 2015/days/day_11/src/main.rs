use std::collections::HashSet;

use lib::run;

type Input<'a> = &'a str;

#[derive(Clone)]
struct Password(u64);

impl Password {
    fn iter(s: &str) -> Self {
        let mut value = 0;
        for ch in s.chars() {
            match ch {
                'a'..='z' => {
                    let x = (ch as u8) - ('a' as u8);
                    value = value * 26 + x as u64;
                }
                _ => panic!("invalid char {}", ch),
            }
        }
        Password(value)
    }
}

impl Iterator for Password {
    type Item = String;

    fn next(&mut self) -> Option<Self::Item> {
        self.0 += 1;
        Some(self.to_string())
    }
}

impl ToString for Password {
    fn to_string(&self) -> String {
        let mut res = String::new();
        let mut value = self.0;
        while value > 0 {
            let x = value % 26;
            value /= 26;
            let ord = (x as u8) + ('a' as u8);
            res.insert(0, ord as char);
        }
        while res.len() < 8 {
            res.insert(0, 'a');
        }
        res
    }
}

fn parse_input(input: &str) -> Input {
    input.trim()
}

fn is_increasing_straight(s: &str) -> bool {
    let mut it = s.chars();
    let mut prev = it.next().unwrap() as u32;
    for ch in it {
        prev += 1;
        if ch as u32 != prev {
            return false;
        }
    }
    true
}

fn contains_increasing_straight(s: &str) -> bool {
    for i in 3..s.len() {
        if is_increasing_straight(&s[i - 3..i]) {
            return true;
        }
    }
    false
}

fn contains_non_overlapping_pairs(s: &str) -> bool {
    (2..s.len() + 1)
        .map(|i| &s[i - 2..i])
        .filter(|sub| sub[0..1] == sub[1..2])
        .collect::<HashSet<_>>()
        .len()
        >= 2
}

fn valid_password(s: &str) -> bool {
    !s.contains(&['i', 'o', 'l'][..])
        && contains_increasing_straight(s)
        && contains_non_overlapping_pairs(s)
}

fn next_password(s: &str) -> String {
    Password::iter(s).find(|s| valid_password(&s)).unwrap()
}

fn part_01(input: &Input) -> String {
    next_password(input)
}

fn part_02(input: &Input) -> String {
    next_password(&next_password(input))
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example_part_1() {
        assert_eq!(valid_password("hijklmmn"), false);
        assert_eq!(valid_password("abbceffg"), false);
        assert_eq!(valid_password("abbcegjk"), false);
        assert_eq!(next_password("abcdefgh"), "abcdffaa");
        assert_eq!(next_password("ghijklmn"), "ghjaabcc");
    }
}
