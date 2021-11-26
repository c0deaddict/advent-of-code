use itertools::Itertools;
use lib::run;
use regex::Regex;
use std::clone::Clone;
use std::cmp::{Eq, PartialEq};
use std::collections::HashMap;
use std::fmt::Debug;

#[derive(Debug, Clone, Eq, PartialEq)]
enum Rule {
    Char(char),
    Seq(Vec<usize>),
    Or(Vec<usize>, Vec<usize>),
}

type Rules = HashMap<usize, Rule>;

#[derive(Debug)]
struct Input<'r> {
    rules: Rules,
    messages: Vec<&'r str>,
}

fn parse_input(input: &str) -> Input {
    let (rules, messages) = input.trim().split("\n\n").collect_tuple().unwrap();

    let re = Regex::new(r#"^(\d+): (?:"(\w)"|(\d+(?: \d+)*)(?: \| (\d+(?: \d+)*))*)$"#).unwrap();

    let rules = rules
        .trim()
        .lines()
        .map(|line| {
            let c = re.captures(line.trim()).unwrap();
            let id = c[1].parse::<usize>().unwrap();
            let rule = if let Some(s) = c.get(2) {
                Rule::Char(s.as_str().chars().next().unwrap())
            } else {
                let seq = c[3].split(' ').map(|s| s.parse().unwrap()).collect();
                if let Some(other) = c.get(4) {
                    let other = other
                        .as_str()
                        .split(' ')
                        .map(|s| s.parse().unwrap())
                        .collect();
                    Rule::Or(seq, other)
                } else {
                    Rule::Seq(seq)
                }
            };
            (id, rule)
        })
        .collect();

    let messages = messages.trim().lines().map(|line| line.trim()).collect();

    Input { rules, messages }
}

fn build_regex(rules: &Rules, start: usize, end: &str) -> Regex {
    fn seq(rules: &Rules, sub_rules: &Vec<usize>) -> String {
        sub_rules
            .iter()
            .map(|rule_id| rec(rules, rule_id))
            .collect()
    }

    fn rec(rules: &Rules, rule_id: &usize) -> String {
        match &rules[rule_id] {
            Rule::Char(ch) => ch.to_string(),
            Rule::Seq(sub_rules) => seq(rules, &sub_rules),
            Rule::Or(a, b) => format!("({}|{})", seq(rules, &a), seq(rules, &b)),
        }
    }

    Regex::new(&format!("^({}){}", rec(rules, &start), end)).unwrap()
}

fn part1(input: &Input) -> usize {
    let re = build_regex(&input.rules, 0, "$");
    input.messages.iter().filter(|m| re.is_match(m)).count()
}

fn re_find_next<'r>(re: &Regex, text: &'r str) -> Option<&'r str> {
    re.find(text).map(|m| &text[m.end()..])
}

fn re_find_count<'r>(re: &Regex, text: &'r str) -> (usize, &'r str) {
    let mut count = 0;
    let mut text = text;
    loop {
        if let Some(next) = re_find_next(re, text) {
            text = next;
            count += 1;
        } else {
            break;
        }
    }
    (count, text)
}

fn part2(input: &Input) -> usize {
    // 0: 8 11
    if input.rules[&0] != Rule::Seq(vec![8, 11]) {
        panic!("Rule 0 should be '8 11'");
    }

    // 8: 42 | 42 8   ==>  8: (42)+
    // 11: 42 31 | 42 11 31   ==> 11: (42){1,n} (31){1,n}
    //
    // combined:
    //
    // 0: (42){1,n} (31){1,m}  where: n > m
    let rule_42 = build_regex(&input.rules, 42, "");
    let rule_31 = build_regex(&input.rules, 31, "");

    input
        .messages
        .iter()
        .filter(|msg| {
            let (count_42, msg) = re_find_count(&rule_42, msg);
            let (count_31, msg) = re_find_count(&rule_31, msg);
            msg.len() == 0 && count_42 > count_31 && count_31 > 0
        })
        .count()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part1, part2)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    0: 4 1 5
    1: 2 3 | 3 2
    2: 4 4 | 5 5
    3: 4 5 | 5 4
    4: \"a\"
    5: \"b\"

    ababbb
    bababa
    abbbab
    aaabbb
    aaaabbb";

    const EXAMPLE_DATA_2: &'static str = "
    42: 9 14 | 10 1
    9: 14 27 | 1 26
    10: 23 14 | 28 1
    1: \"a\"
    11: 42 31
    5: 1 14 | 15 1
    19: 14 1 | 14 14
    12: 24 14 | 19 1
    16: 15 1 | 14 14
    31: 14 17 | 1 13
    6: 14 14 | 1 14
    2: 1 24 | 14 4
    0: 8 11
    13: 14 3 | 1 12
    15: 1 | 14
    17: 14 2 | 1 7
    23: 25 1 | 22 14
    28: 16 1
    4: 1 1
    20: 14 14 | 1 15
    3: 5 14 | 16 1
    27: 1 6 | 14 18
    14: \"b\"
    21: 14 1 | 1 14
    25: 1 1 | 1 14
    22: 14 14
    8: 42
    26: 14 22 | 1 20
    18: 15 15
    7: 14 5 | 1 21
    24: 14 1

    abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
    bbabbbbaabaabba
    babbbbaabbbbbabbbbbbaabaaabaaa
    aaabbbbbbaaaabaababaabababbabaaabbababababaaa
    bbbbbbbaaaabbbbaaabbabaaa
    bbbababbbbaaaaaaaabbababaaababaabab
    ababaaaaaabaaab
    ababaaaaabbbaba
    baabbaaaabbaaaababbaababb
    abbbbabbbbaaaababbbbbbaaaababb
    aaaaabbaabaaaaababaa
    aaaabbaaaabbaaa
    aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
    babaaabbbaaabaababbaabababaaab
    aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba";

    #[test]
    fn example_1_part1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part1(&input), 2);
    }

    #[test]
    fn example_1_part2() {
        let input = parse_input(EXAMPLE_DATA_2);
        assert_eq!(part2(&input), 12);
    }
}
