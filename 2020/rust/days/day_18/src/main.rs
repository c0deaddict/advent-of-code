use lib::run;
use regex::Regex;
use std::clone::Clone;
use std::cmp::{Eq, PartialEq};
use std::fmt::Debug;
use std::result::Result;

#[derive(Debug, Eq, PartialEq, Copy, Clone)]
enum Token {
    Number(i64),
    Add,
    Times,
    OpenParen,
    CloseParen,
}

type Input = Vec<Vec<Token>>;
type ParseResult<'r> = Result<(&'r [Token], i64), &'static str>;
type Parser = fn(&[Token]) -> ParseResult;

fn parse_input(input: &str) -> Input {
    let re = Regex::new(r"\d+|[\+\*\(\)]").unwrap();

    input
        .trim()
        .lines()
        .map(|line| {
            re.captures_iter(line.trim())
                .map(|c| match &c[0] {
                    "+" => Token::Add,
                    "*" => Token::Times,
                    "(" => Token::OpenParen,
                    ")" => Token::CloseParen,
                    i => Token::Number(i.parse().unwrap()),
                })
                .collect()
        })
        .collect()
}

fn parse_prim(input: &[Token], parse_expr: Parser) -> ParseResult {
    match input.get(0) {
        None => Err("expected a primitive"),
        Some(Token::Number(i)) => Ok((&input[1..], *i)),
        Some(Token::OpenParen) => parse_expr(&input[1..]).and_then(|(input, res)| {
            if input.get(0) != Some(&Token::CloseParen) {
                Err("expected close paren")
            } else {
                Ok((&input[1..], res))
            }
        }),
        _ => Err("expected a primitive"),
    }
}

fn match_operator<'a>(token: Option<&'a Token>) -> Option<&'a Token> {
    match token {
        Some(t) if t == &Token::Add || t == &Token::Times => Some(t),
        _ => None,
    }
}

fn parse_prim_part1(input: &[Token]) -> ParseResult {
    parse_prim(input, parse_part1)
}

fn parse_part1(input: &[Token]) -> ParseResult {
    parse_prim_part1(input).and_then(|(mut input, mut lhs)| loop {
        if let Some(op) = match_operator(input.get(0)) {
            match parse_prim_part1(&input[1..]) {
                Ok((next, rhs)) => {
                    if op == &Token::Add {
                        lhs += rhs
                    } else {
                        lhs *= rhs
                    };
                    input = next;
                }
                err => return err,
            }
        } else {
            return Ok((input, lhs));
        }
    })
}

fn parse_line(input: &[Token], parser: Parser) -> Result<i64, &'static str> {
    parser(input).and_then(|(input, res)| {
        if input.len() > 0 {
            Err("expected end")
        } else {
            Ok(res)
        }
    })
}

fn part1(input: &Input) -> i64 {
    input
        .iter()
        .map(|line| parse_line(line, parse_part1).unwrap())
        .sum()
}

fn parse_prim_part2(input: &[Token]) -> ParseResult {
    parse_prim(input, parse_times)
}

fn parse_add(input: &[Token]) -> ParseResult {
    parse_prim_part2(input).and_then(|(input, lhs)| {
        if input.get(0) == Some(&Token::Add) {
            parse_add(&input[1..]).map(|(input, rhs)| (input, lhs + rhs))
        } else {
            Ok((input, lhs))
        }
    })
}

fn parse_times(input: &[Token]) -> ParseResult {
    parse_add(input).and_then(|(input, lhs)| {
        if input.get(0) == Some(&Token::Times) {
            parse_times(&input[1..]).map(|(input, rhs)| (input, lhs * rhs))
        } else {
            Ok((input, lhs))
        }
    })
}

fn part2(input: &Input) -> i64 {
    input
        .iter()
        .map(|line| parse_line(line, parse_times).unwrap())
        .sum()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part1, part2)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXPR_1: &'static str = "1 + 2 * 3 + 4 * 5 + 6";
    const EXPR_2: &'static str = "1 + (2 * 3) + (4 * (5 + 6))";
    const EXPR_3: &'static str = "2 * 3 + (4 * 5)";
    const EXPR_4: &'static str = "5 + (8 * 3 + 9 + 3 * 4 * 3)";
    const EXPR_5: &'static str = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))";
    const EXPR_6: &'static str = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2";

    #[test]
    fn example_1_part1() {
        assert_eq!(part1(&parse_input(EXPR_1)), 71);
    }

    #[test]
    fn example_2_part1() {
        assert_eq!(part1(&parse_input(EXPR_2)), 51);
    }

    #[test]
    fn example_3_part1() {
        assert_eq!(part1(&parse_input(EXPR_3)), 26);
    }

    #[test]
    fn example_4_part1() {
        assert_eq!(part1(&parse_input(EXPR_4)), 437);
    }

    #[test]
    fn example_5_part1() {
        assert_eq!(part1(&parse_input(EXPR_5)), 12240);
    }

    #[test]
    fn example_6_part1() {
        assert_eq!(part1(&parse_input(EXPR_6)), 13632);
    }

    #[test]
    fn example_1_part2() {
        assert_eq!(part2(&parse_input(EXPR_1)), 231);
    }

    #[test]
    fn example_2_part2() {
        assert_eq!(part2(&parse_input(EXPR_2)), 51);
    }

    #[test]
    fn example_3_part2() {
        assert_eq!(part2(&parse_input(EXPR_3)), 46);
    }

    #[test]
    fn example_4_part2() {
        assert_eq!(part2(&parse_input(EXPR_4)), 1445);
    }

    #[test]
    fn example_5_part2() {
        assert_eq!(part2(&parse_input(EXPR_5)), 669060);
    }

    #[test]
    fn example_6_part2() {
        assert_eq!(part2(&parse_input(EXPR_6)), 23340);
    }
}
