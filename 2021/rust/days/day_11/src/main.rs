use lib::run;
use std::collections::{HashMap, HashSet};

#[derive(Debug, Hash, Eq, PartialEq, Copy, Clone)]
struct Position {
    x: i32,
    y: i32,
}

type Input = HashMap<Position, usize>;

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .lines()
        .enumerate()
        .flat_map(|(y, l)| {
            l.trim()
                .chars()
                .enumerate()
                .map(|(x, h)| {
                    let x = x as i32;
                    let y = y as i32;
                    (Position { x, y }, h.to_string().parse().unwrap())
                })
                .collect::<Vec<_>>()
        })
        .collect()
}

fn neighbours(pos: &Position) -> Vec<Position> {
    [
        (-1, 1),
        (-1, 0),
        (-1, -1),
        (0, -1),
        (1, -1),
        (1, 0),
        (1, 1),
        (0, 1),
    ]
    .iter()
    .map(|(x, y)| Position {
        x: pos.x + x,
        y: pos.y + y,
    })
    .collect()
}

fn step(state: &mut Input) -> usize {
    let mut flashes = 0;

    let mut queue: Vec<_> = state.keys().cloned().collect();
    while let Some(pos) = queue.pop() {
        state.entry(pos).and_modify(|energy| {
            *energy += 1;
            // Reset later, octopuses can only flash once per step.
            if *energy == 10 {
                flashes += 1;
                for n in neighbours(&pos) {
                    queue.push(n);
                }
            }
        });
    }

    // Reset energy.
    for (_, energy) in state {
        if *energy > 9 {
            *energy = 0;
        }
    }

    return flashes;
}

fn part_01(input: &Input) -> usize {
    let mut state = input.clone();
    let mut flashes = 0;
    for _ in 0..100 {
        flashes += step(&mut state);
    }
    return flashes;
}

fn part_02(input: &Input) -> usize {
    let mut state = input.clone();
    for i in 0.. {
        if state.values().sum::<usize>() == 0 {
            return i;
        }
        step(&mut state);
    }
    panic!("unreachable");
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    5483143223
    2745854711
    5264556173
    6141336146
    6357385478
    4167524645
    2176841721
    6882881134
    4846848554
    5283751526
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 1656)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 195)
    }
}
