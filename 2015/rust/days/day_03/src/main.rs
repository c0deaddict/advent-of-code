use lib::run;
use std::collections::HashSet;

#[derive(Debug, Clone, Eq, PartialEq)]
enum Direction {
    North,
    South,
    East,
    West,
}

#[derive(Debug, Clone, Eq, PartialEq, Hash)]
struct Position {
    x: i32,
    y: i32,
}

type Input = Vec<Direction>;

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .chars()
        .map(|ch| match ch {
            '^' => Direction::North,
            'v' => Direction::South,
            '>' => Direction::East,
            '<' => Direction::West,
            _ => panic!("unknown direction {}", ch),
        })
        .collect()
}

fn visit<'a, I>(input: I) -> HashSet<Position>
where
    I: Iterator<Item = &'a Direction>,
{
    let mut pos = Position { x: 0, y: 0 };
    let mut visited = HashSet::new();
    visited.insert(pos.clone());

    for dir in input {
        match dir {
            Direction::North => pos.y -= 1,
            Direction::South => pos.y += 1,
            Direction::East => pos.x += 1,
            Direction::West => pos.x -= 1,
        }
        visited.insert(pos.clone());
    }

    visited
}

fn part_01(input: &Input) -> usize {
    visit(input.iter()).len()
}

fn part_02(input: &Input) -> usize {
    let mut visited = HashSet::new();
    visited.extend(visit(input.iter().step_by(2)));
    visited.extend(visit(input.iter().skip(1).step_by(2)));
    visited.len()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example1_part_1() {
        assert_eq!(part_01(&parse_input("^>v<")), 4)
    }

    #[test]
    fn example2_part_1() {
        assert_eq!(part_01(&parse_input("^v^v^v^v^v")), 2)
    }

    #[test]
    fn example1_part_2() {
        assert_eq!(part_02(&parse_input("^>v<")), 3)
    }

    #[test]
    fn example2_part_2() {
        assert_eq!(part_02(&parse_input("^v^v^v^v^v")), 11)
    }
}
