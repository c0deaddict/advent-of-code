use itertools::Itertools;
use lib::run;
use std::fmt::Debug;

use Snailfish::*;

#[derive(Eq, PartialEq, Clone)]
enum Snailfish {
    Pair(Box<Snailfish>, Box<Snailfish>),
    Regular(u8),
}

impl ToString for Snailfish {
    fn to_string(&self) -> String {
        match self {
            Pair(a, b) => format!("[{},{}]", a.to_string(), b.to_string()),
            Regular(n) => n.to_string(),
        }
    }
}

impl Debug for Snailfish {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.to_string())
    }
}

impl Snailfish {
    fn parse(s: &str) -> Snailfish {
        fn parse_rec<'a>(s: &'a str) -> (&'a str, Snailfish) {
            match &s[0..=0] {
                "[" => {
                    let (s, left) = parse_rec(&s[1..]);
                    if &s[0..=0] != "," {
                        panic!("expected a comma");
                    }
                    let (s, right) = parse_rec(&s[1..]);
                    if &s[0..=0] != "]" {
                        panic!("expected a end brace");
                    }
                    (&s[1..], Pair(Box::new(left), Box::new(right)))
                }
                n => (&s[1..], Regular(n.parse().unwrap())),
            }
        }

        let (s, res) = parse_rec(s);
        if s.len() > 0 {
            panic!("expected EOF after expression, got: {}", s);
        }

        return res;
    }

    fn magnitude(&self) -> u64 {
        match self {
            Regular(n) => *n as u64,
            Pair(left, right) => 3 * left.magnitude() + 2 * right.magnitude(),
        }
    }

    fn as_regular(&self) -> Option<u8> {
        match self {
            Regular(n) => Some(*n),
            _ => None,
        }
    }

    fn add_left(&mut self, value: u8) {
        match self {
            Regular(n) => *n += value,
            Pair(left, _) => left.add_left(value),
        }
    }

    fn add_right(&mut self, value: u8) {
        match self {
            Regular(n) => *n += value,
            Pair(_, right) => right.add_right(value),
        }
    }

    fn explode(&mut self, depth: usize) -> Option<(u8, u8)> {
        match self {
            Pair(left, right) if depth >= 4 => {
                let left = left.as_regular().unwrap();
                let right = right.as_regular().unwrap();
                *self = Regular(0);
                Some((left, right))
            }
            Pair(left, right) => match left.explode(depth + 1) {
                Some((l, r)) => {
                    if r != 0 {
                        right.add_left(r);
                    }
                    Some((l, 0))
                }
                None => match right.explode(depth + 1) {
                    Some((l, r)) => {
                        if l != 0 {
                            left.add_right(l);
                        }
                        Some((0, r))
                    }
                    other => other,
                },
            },
            Regular(_) => None,
        }
    }

    fn split(&mut self, depth: usize) -> bool {
        match self {
            Pair(left, right) => left.split(depth + 1) || right.split(depth + 1),
            Regular(n) if *n >= 10 => {
                let left = Regular(*n / 2);
                let right = Regular((*n + 1) / 2);
                *self = Pair(Box::new(left), Box::new(right));
                return true;
            }
            Regular(_) => false,
        }
    }

    fn action(&mut self) -> bool {
        self.explode(0).is_some() || self.split(0)
    }

    fn reduce(&mut self) {
        while self.action() {}
    }

    fn add(&self, other: &Snailfish) -> Snailfish {
        let mut res = Pair(Box::new(self.clone()), Box::new(other.clone()));
        res.reduce();
        return res;
    }
}

type Input = Vec<Snailfish>;

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .lines()
        .map(|l| Snailfish::parse(l.trim()))
        .collect()
}

fn sum_list(input: &Input) -> Snailfish {
    input.iter().cloned().reduce(|a, b| a.add(&b)).unwrap()
}

fn part_01(input: &Input) -> u64 {
    sum_list(input).magnitude()
}

fn part_02(input: &Input) -> u64 {
    input
        .iter()
        .permutations(2)
        .map(|v| v[0].add(v[1]).magnitude())
        .max()
        .unwrap()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_reduce() {
        for (expr, res) in [
            ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
            ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
            ("[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"),
            (
                "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
                "[[3,[2,[8,0]]],[9,[5,[7,0]]]]",
            ),
            (
                "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]",
                "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]",
            ),
        ] {
            let mut n = Snailfish::parse(expr);
            n.reduce();
            assert_eq!(n.to_string(), res);
        }
    }

    #[test]
    fn test_sum_list_1() {
        let res = sum_list(&parse_input("[1,1]\n[2,2]\n[3,3]\n[4,4]"));
        assert_eq!(res.to_string(), "[[[[1,1],[2,2]],[3,3]],[4,4]]");
    }

    #[test]
    fn test_sum_list_2() {
        let res = sum_list(&parse_input("[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]"));
        assert_eq!(res.to_string(), "[[[[3,0],[5,3]],[4,4]],[5,5]]");
    }

    #[test]
    fn test_sum_list_3() {
        let res = sum_list(&parse_input("[1,1]\n[2,2]\n[3,3]\n[4,4]\n[5,5]\n[6,6]"));
        assert_eq!(res.to_string(), "[[[[5,0],[7,4]],[5,5]],[6,6]]");
    }

    const EXAMPLE_DATA_1: &'static str = "
    [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
    [[[5,[2,8]],4],[5,[[9,9],0]]]
    [6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
    [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
    [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
    [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
    [[[[5,4],[7,7]],8],[[8,3],8]]
    [[9,3],[[9,9],[6,[4,9]]]]
    [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
    [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 4140)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 3993)
    }
}
