use itertools::Itertools;
use lib::run;

type Input<'a> = Vec<&'a str>;

fn parse_input(input: &str) -> Input {
    input.trim().lines().map(|l| l.trim()).collect()
}

fn open_char(ch: char) -> char {
    match ch {
        ')' => '(',
        ']' => '[',
        '}' => '{',
        '>' => '<',
        _ => panic!("unexpected char {}", ch),
    }
}

fn syntax_check(line: &str) -> Option<char> {
    let mut stack = vec![];
    for ch in line.chars() {
        match ch {
            '(' | '[' | '{' | '<' => {
                stack.push(ch);
            }
            ')' | ']' | '}' | '>' => {
                match stack.pop() {
                    None => return None,
                    Some(open) => {
                        if open != open_char(ch) {
                            return Some(ch);
                        }
                    }
                };
            }
            _ => panic!("unexpected char {}", ch),
        }
    }

    return None;
}

fn part_01(input: &Input) -> usize {
    input
        .iter()
        .filter_map(|line| {
            syntax_check(line).map(|ch| match ch {
                ')' => 3,
                ']' => 57,
                '}' => 1197,
                '>' => 25137,
                _ => panic!("unexpected char {}", ch),
            })
        })
        .sum()
}

fn autocomplete(line: &str) -> Option<String> {
    let mut stack = vec![];
    for ch in line.chars() {
        match ch {
            '(' | '[' | '{' | '<' => {
                stack.push(ch);
            }
            ')' | ']' | '}' | '>' => {
                match stack.pop() {
                    None => return None,
                    Some(open) => {
                        if open != open_char(ch) {
                            return None; // Corrupted.
                        }
                    }
                };
            }
            _ => panic!("unexpected char {}", ch),
        }
    }

    return Some(stack.iter().rev().collect::<String>());
}

fn autocomplete_score(s: &str) -> usize {
    let mut score = 0;
    for ch in s.chars() {
        score *= 5;
        score += match ch {
            '(' => 1,
            '[' => 2,
            '{' => 3,
            '<' => 4,
            _ => panic!("unexpected char {}", ch),
        };
    }
    return score;
}

fn part_02(input: &Input) -> usize {
    let scores: Vec<_> = input
        .iter()
        .filter_map(|line| autocomplete(line).map(|s| autocomplete_score(&s)))
        .sorted()
        .collect();

    scores[scores.len() / 2]
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    [({(<(())[]>[[{[]{<()<>>
    [(()[<>])]({[<{<<[]>>(
    {([(<{}[<>[]}>{[]{[(<()>
    (((({<>}<{<{<>}{[]{[]{}
    [[<[([]))<([[{}[[()]]]
    [{[{({}]{}}([{[{{{}}([]
    {<[[]]>}<{[{[{[]{()[[[]
    [<(<(<(<{}))><([]([]()
    <{([([[(<>()){}]>(<<{{
    <{([{{}}[<[[[<>{}]]]>[]]
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 26397)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 288957);
    }
}
