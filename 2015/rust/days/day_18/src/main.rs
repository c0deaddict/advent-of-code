use lib::run;
use std::collections::HashMap;

#[derive(Debug, Hash, PartialEq, Eq, Clone)]
struct Position {
    x: i32,
    y: i32,
}

type Input = HashMap<Position, bool>;

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .lines()
        .enumerate()
        .flat_map(|(y, l)| {
            l.trim()
                .chars()
                .enumerate()
                .map(|(x, c)| {
                    let pos = Position {
                        x: x as i32,
                        y: y as i32,
                    };
                    (pos, c == '#')
                })
                .collect::<Vec<_>>()
        })
        .collect()
}

const NEIGHBOUR_OFFSETS: [(i32, i32); 8] = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
];

fn count_neighbours(state: &Input, pos: &Position) -> usize {
    NEIGHBOUR_OFFSETS
        .iter()
        .map(|(x, y)| Position {
            x: pos.x + x,
            y: pos.y + y,
        })
        .filter_map(|p| state.get(&p))
        .filter(|v| **v)
        .count()
}

fn compute_steps(input: &Input, steps: usize) -> usize {
    let mut state = input.clone();
    for _ in 0..steps {
        state = state
            .iter()
            .map(|(pos, value)| {
                let neighbours = count_neighbours(&state, pos);
                let value = if *value {
                    neighbours == 2 || neighbours == 3
                } else {
                    neighbours == 3
                };

                (pos.clone(), value)
            })
            .collect();
    }

    state.iter().filter(|(_, v)| **v).count()
}

fn part_01(input: &Input) -> usize {
    compute_steps(input, 100)
}

fn compute_part2(input: &Input, steps: usize) -> usize {
    let max_x = input.keys().max_by_key(|p| p.x).unwrap().x;
    let max_y = input.keys().max_by_key(|p| p.y).unwrap().y;

    let corners = [
        Position { x: 0, y: 0 },
        Position { x: max_x, y: 0 },
        Position { x: 0, y: max_y },
        Position { x: max_x, y: max_y },
    ];

    let mut state = input.clone();
    for pos in &corners {
        state.insert(pos.clone(), true);
    }

    for _ in 0..steps {
        state = state
            .iter()
            .map(|(pos, value)| {
                let neighbours = count_neighbours(&state, pos);
                let value = if corners.contains(pos) {
                    true
                } else if *value {
                    neighbours == 2 || neighbours == 3
                } else {
                    neighbours == 3
                };

                (pos.clone(), value)
            })
            .collect();
    }

    state.iter().filter(|(_, v)| **v).count()
}

fn part_02(input: &Input) -> usize {
    compute_part2(input, 100)
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    .#.#.#
    ...##.
    #....#
    ..#...
    #.#..#
    ####..
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(compute_steps(&input, 4), 4)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(compute_part2(&input, 5), 17)
    }
}
