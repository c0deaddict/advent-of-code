use itertools::Itertools;
use lib::run;

struct Position {
    x: i32,
    y: i32,
}

type Input<'a> = Vec<(&'a str, i32)>;

fn parse_input(input: &str) -> Input {
    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| {
            let (dir, amount) = l.split_whitespace().collect_tuple().unwrap();
            (dir, amount.parse().unwrap())
        })
        .collect()
}

fn part_01(input: &Input) -> i32 {
    let mut pos = Position { x: 0, y: 0 };
    for (dir, amount) in input {
        match *dir {
            "forward" => pos.x += amount,
            "down" => pos.y += amount,
            "up" => pos.y -= amount,
            _ => panic!("unknown direction {}", dir),
        }
    }
    pos.x * pos.y
}

fn part_02(input: &Input) -> i32 {
    let mut aim = 0;
    let mut pos = Position { x: 0, y: 0 };
    for (dir, amount) in input {
        match *dir {
            "forward" => {
                pos.x += amount;
                pos.y += aim * amount;
            }
            "down" => aim += amount,
            "up" => aim -= amount,
            _ => panic!("unknown direction {}", dir),
        }
    }
    pos.x * pos.y
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    forward 5
    down 5
    forward 8
    up 3
    down 8
    forward 2
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 150)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 900)
    }
}
