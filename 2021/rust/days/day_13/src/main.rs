use itertools::Itertools;
use regex::Regex;
use std::collections::HashSet;

use lib::run;

#[derive(Debug, Hash, Eq, PartialEq, Copy, Clone)]
struct Position {
    x: i32,
    y: i32,
}

#[derive(Debug)]
enum Fold {
    Up(i32),
    Left(i32),
}

impl Fold {
    fn apply(&self, pos: &Position) -> Option<Position> {
        match self {
            Self::Up(y) if pos.y == *y => None,
            Self::Up(y) if pos.y > *y => Some(Position {
                x: pos.x,
                y: pos.y - (pos.y - *y) * 2,
            }),
            Self::Left(x) if pos.x == *x => None,
            Self::Left(x) if pos.x > *x => Some(Position {
                x: pos.x - (pos.x - *x) * 2,
                y: pos.y,
            }),
            _ => Some(pos.clone()),
        }
    }
}

type Paper = HashSet<Position>;

#[derive(Debug)]
struct Input {
    paper: Paper,
    folds: Vec<Fold>,
}

fn parse_input(input: &str) -> Input {
    let fold_re = Regex::new(r"^fold along (x|y)=(\d+)$").unwrap();
    let (paper, folds) = input.trim().splitn(2, "\n\n").collect_tuple().unwrap();

    let paper = paper
        .trim()
        .lines()
        .map(|l| {
            let (x, y) = l
                .trim()
                .splitn(2, ",")
                .map(|s| s.parse().unwrap())
                .collect_tuple()
                .unwrap();
            Position { x, y }
        })
        .collect();

    let folds = folds
        .trim()
        .lines()
        .map(|l| {
            let c = fold_re.captures(l.trim()).unwrap();
            let i = c.get(2).unwrap().as_str().parse().unwrap();
            match c.get(1).unwrap().as_str() {
                "x" => Fold::Left(i),
                "y" => Fold::Up(i),
                axis => panic!("unexpected fold {}", axis),
            }
        })
        .collect();

    Input { paper, folds }
}

fn do_fold(paper: &Paper, fold: &Fold) -> Paper {
    paper.iter().filter_map(|pos| fold.apply(pos)).collect()
}

fn part_01(input: &Input) -> usize {
    do_fold(&input.paper, &input.folds[0]).len()
}

fn print(paper: &Paper) {
    let maxx = paper.iter().max_by_key(|p| p.x).unwrap().x;
    let maxy = paper.iter().max_by_key(|p| p.y).unwrap().y;
    for y in 0..=maxy {
        for x in 0..=maxx {
            if paper.contains(&Position { x, y }) {
                print!("#");
            } else {
                print!(" ");
            }
        }
        println!("");
    }
}

fn part_02(input: &Input) -> () {
    let mut paper = input.paper.clone();
    for fold in &input.folds {
        paper = do_fold(&paper, &fold);
    }
    print(&paper);
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    6,10
    0,14
    9,10
    0,3
    10,4
    4,11
    6,0
    6,12
    4,1
    0,13
    10,12
    3,4
    3,0
    8,4
    1,10
    2,14
    8,10
    9,0

    fold along y=7
    fold along x=5
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 17)
    }
}
