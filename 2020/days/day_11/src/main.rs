use lib::run;
use std::cmp::{Eq, PartialEq};
use std::fmt::Debug;
use std::hash::Hash;
use std::option::Option;

#[derive(PartialEq, Eq, Hash, Debug)]
struct Point {
    x: usize,
    y: usize,
}

impl Point {
    fn move_dir(&self, dir: &Dir) -> Option<Point> {
        let x = self.x as isize + dir.0;
        let y = self.y as isize + dir.1;
        if x < 0 || y < 0 {
            None
        } else {
            Some(Point {
                x: x as usize,
                y: y as usize,
            })
        }
    }
}

type Dir = (isize, isize);

const DIRECTIONS: &'static [Dir] = &[
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (1, -1),
    (1, 0),
    (1, 1),
    (0, 1),
];

type Input = Vec<Vec<char>>;

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .lines()
        .map(|line| line.trim().chars().collect())
        .collect()
}

fn neighbours(p: &Point) -> Vec<Point> {
    DIRECTIONS.iter().filter_map(|d| p.move_dir(d)).collect()
}

fn get_cell<'r>(input: &'r Input, p: &Point) -> Option<&'r char> {
    input.get(p.y).and_then(|row| row.get(p.x))
}

fn occupied_neighbours(input: &Input, p: &Point) -> usize {
    neighbours(p)
        .iter()
        .filter_map(|p| get_cell(input, p))
        .filter(|cell| **cell == '#')
        .count()
}

fn count_occupied(input: &Input) -> usize {
    input
        .iter()
        .map(|row| row.iter().filter(|cell| **cell == '#').count())
        .sum()
}

fn tick(input: &Input, f: fn(&Input, &Point, &char) -> char) -> Input {
    input
        .iter()
        .enumerate()
        .map(|(y, row)| {
            row.iter()
                .enumerate()
                .map(|(x, cell)| f(input, &Point { x, y }, cell))
                .collect()
        })
        .collect()
}

fn change_part1(input: &Input, p: &Point, cell: &char) -> char {
    match cell {
        '.' => '.',
        'L' => {
            if occupied_neighbours(input, &p) == 0 {
                '#'
            } else {
                'L'
            }
        }
        '#' => {
            if occupied_neighbours(input, &p) >= 4 {
                'L'
            } else {
                '#'
            }
        }
        _ => panic!("unexpected char {}", cell),
    }
}

fn iterate_part1(input: &Input) -> Input {
    let next = tick(input, change_part1);
    if &next == input {
        return next;
    }
    iterate_part1(&next)
}

fn part1(input: &Input) -> usize {
    count_occupied(&iterate_part1(input))
}

fn find_seat<'r>(input: &'r Input, p: &Point, dir: &Dir) -> Option<&'r char> {
    p.move_dir(dir).and_then(|p| match get_cell(input, &p) {
        Some('.') => find_seat(input, &p, dir),
        other => other,
    })
}

fn occupied_visible_seats(input: &Input, p: &Point) -> usize {
    DIRECTIONS
        .iter()
        .filter_map(|d| find_seat(input, p, d))
        .filter(|cell| **cell == '#')
        .count()
}

fn change_part2(input: &Input, p: &Point, cell: &char) -> char {
    match cell {
        '.' => '.',
        'L' => {
            if occupied_visible_seats(input, &p) == 0 {
                '#'
            } else {
                'L'
            }
        }
        '#' => {
            if occupied_visible_seats(input, &p) >= 5 {
                'L'
            } else {
                '#'
            }
        }
        _ => panic!("unexpected char {}", cell),
    }
}

fn iterate_part2(input: &Input) -> Input {
    let next = tick(input, change_part2);
    if &next == input {
        return next;
    }
    iterate_part2(&next)
}

fn part2(input: &Input) -> usize {
    count_occupied(&iterate_part2(input))
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part1, part2)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    L.LL.LL.LL
    LLLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLLL
    L.LLLLLL.L
    L.LLLLL.LL";

    #[test]
    fn example_1_part1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part1(&input), 37);
    }

    #[test]
    fn example_1_part2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part2(&input), 26);
    }
}
