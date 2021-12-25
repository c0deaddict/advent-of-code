use lib::run;
use std::collections::HashMap;

#[derive(Debug, Hash, Eq, PartialEq, Copy, Clone)]
struct Position {
    x: i32,
    y: i32,
}

#[derive(Debug, Eq, PartialEq, Copy, Clone)]
enum Cucumber {
    East,
    South,
}

#[derive(Debug, Eq, PartialEq, Clone)]
struct SeaFloor {
    cucumbers: HashMap<Position, Cucumber>,
    width: i32,
    height: i32,
}

type Input = SeaFloor;

fn parse_input(input: &str) -> Input {
    let cucumbers: HashMap<_, _> = input
        .trim()
        .lines()
        .enumerate()
        .flat_map(|(y, l)| {
            l.trim()
                .chars()
                .enumerate()
                .filter_map(|(x, c)| {
                    if c == '.' {
                        return None;
                    }
                    let x = x as i32;
                    let y = y as i32;
                    let cucumber = if c == '>' {
                        Cucumber::East
                    } else {
                        Cucumber::South
                    };
                    Some((Position { x, y }, cucumber))
                })
                .collect::<Vec<_>>()
        })
        .collect();

    let width = 1 + cucumbers.keys().max_by_key(|p| p.x).unwrap().x;
    let height = 1 + cucumbers.keys().max_by_key(|p| p.y).unwrap().y;
    SeaFloor {
        cucumbers,
        width,
        height,
    }
}

fn next_position(state: &SeaFloor, cucumber: &Cucumber, pos: &Position) -> Position {
    match cucumber {
        Cucumber::East => Position {
            x: (pos.x + 1) % state.width,
            y: pos.y,
        },
        Cucumber::South => Position {
            x: pos.x,
            y: (pos.y + 1) % state.height,
        },
    }
}

fn step_wave(state: &SeaFloor, wave: &Cucumber) -> SeaFloor {
    let mut result = state.clone();
    for (pos, cucumber) in state.cucumbers.iter() {
        if cucumber != wave {
            continue;
        }

        let next = next_position(&state, &cucumber, &pos);
        if !state.cucumbers.contains_key(&next) {
            result.cucumbers.remove(pos);
            result.cucumbers.insert(next, *cucumber);
        }
    }
    return result;
}

fn step(state: &SeaFloor) -> SeaFloor {
    step_wave(&step_wave(&state, &Cucumber::East), &Cucumber::South)
}

fn part_01(input: &Input) -> usize {
    let mut state = input.clone();
    for i in 1.. {
        let next = step(&state);
        if next == state {
            return i;
        }
        state = next;
    }
    panic!("unreachable");
}

fn part_02(input: &Input) -> usize {
    0
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    v...>>.vv>
    .vv>>.vv..
    >>.>v>...v
    >>v>>.>.v.
    v>v.vv.v..
    >.>>..v...
    .vv..>.>v.
    v.v..>>v.v
    ....v..v.>
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 58)
    }
}
