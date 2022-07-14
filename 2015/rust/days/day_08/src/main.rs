use lib::run;
use std::iter::FromIterator;

type Input<'a> = Vec<&'a str>;

fn parse_input(input: &str) -> Input {
    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .collect()
}

fn unescape(s: &str) -> String {
    let mut res = String::new();
    let mut it = s.chars();
    if it.next().unwrap() != '"' {
        panic!("expected string to start with quote");
    }
    while let Some(ch) = it.next() {
        match ch {
            '"' => {
                if it.next().is_some() {
                    panic!("string does not end after quote");
                }
                return res;
            }
            '\\' => match it.next().unwrap() {
                'x' => {
                    let hex = String::from_iter(vec![it.next().unwrap(), it.next().unwrap()]);
                    let codepoint = u32::from_str_radix(&hex, 16).unwrap();
                    res.push(char::from_u32(codepoint).unwrap());
                }
                ch => res.push(ch),
            },
            _ => res.push(ch),
        }
    }

    panic!("unexpected end of string");
}

fn part_01(input: &Input) -> usize {
    let code: usize = input.iter().map(|l| l.len()).sum();
    let escaped: usize = input.iter().map(|l| unescape(l).chars().count()).sum();
    code - escaped
}

fn escape(s: &str) -> String {
    let mut res = "\"".to_owned();
    for ch in s.chars() {
        match ch {
            '"' | '\\' => {
                res.push('\\');
                res.push(ch);
            }
            _ => res.push(ch),
        }
    }
    res.push('"');
    res
}

fn part_02(input: &Input) -> usize {
    let escaped: usize = input.iter().map(|l| escape(l).len()).sum();
    let original: usize = input.iter().map(|l| l.len()).sum();
    escaped - original
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = r#"
    ""
    "abc"
    "aaa\"aaa"
    "\x27"
    "#;

    #[test]
    fn test_unescape() {
        assert_eq!(unescape(r#""abc""#), "abc");
        assert_eq!(unescape(r#""aaa\"aaa""#), "aaa\"aaa");
        assert_eq!(unescape(r#""\x27""#), "\x27");
        assert_eq!(unescape(r#""\\""#), "\\");
        assert_eq!(unescape(r#""\x27""#).len(), 1);
    }

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 12)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 19)
    }
}
