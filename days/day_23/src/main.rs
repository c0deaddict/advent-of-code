use lib::run;
use std::collections::HashMap;

struct Ring {
    map: HashMap<u32, u32>,
    min: u32,
    max: u32,
    current: u32,
}

impl Ring {
    fn new(data: &[u32]) -> Self {
        let min = *data.iter().min().unwrap();
        let max = *data.iter().max().unwrap();
        let current = data[0];

        let map = data
            .iter()
            .cloned()
            .enumerate()
            .map(|(i, value)| {
                let next = data[(i + 1) % data.len()];
                (value, next)
            })
            .collect();

        Ring {
            min,
            max,
            current,
            map,
        }
    }

    fn get_next(&self, value: u32) -> Option<u32> {
        self.map.get(&value).map(|v| *v)
    }

    fn move_current(&mut self) {
        self.current = self.get_next(self.current).unwrap();
    }

    fn pop(&mut self) -> u32 {
        let value = self.get_next(self.current).unwrap();
        let next = self.get_next(value).unwrap();
        *self.map.get_mut(&self.current).unwrap() = next;
        value
    }

    fn push(&mut self, after: u32, value: u32) {
        let next = self.map.get(&after).unwrap();
        *self.map.get_mut(&value).unwrap() = *next;
        *self.map.get_mut(&after).unwrap() = value;
    }
}

type Input = Vec<u32>;

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .chars()
        .map(|d| d.to_string().parse().unwrap())
        .collect()
}

fn do_move(ring: &mut Ring) {
    // Pick up three cups.
    let pick_up = (0..3).map(|_| ring.pop()).collect::<Vec<_>>();

    // Choose destination, decrementing each time value is in pick_up.
    let mut dest = ring.current - 1;
    for _ in 0..3 {
        if dest < ring.min {
            dest = ring.max;
        }
        if pick_up.contains(&dest) {
            dest -= 1;
        }
    }

    // Push values after destination.
    for value in pick_up.iter().rev() {
        ring.push(dest, *value);
    }

    ring.move_current();
}

fn labels(ring: &Ring) -> String {
    let mut res = vec![];
    let mut value = ring.get_next(1).unwrap();
    loop {
        res.push(value.to_string());
        value = ring.get_next(value).unwrap();
        if value == 1 {
            break;
        }
    }
    res.join("")
}

fn play(input: &Input, moves: usize) -> Ring {
    let mut ring = Ring::new(input);
    for _ in 0..moves {
        do_move(&mut ring);
    }
    ring
}

fn part1(input: &Input) -> String {
    labels(&play(input, 100))
}

fn extend_input(input: &Input) -> Input {
    let mut val = *input.iter().max().unwrap();
    let mut res = input.clone();
    while res.len() < 1_000_000 {
        val += 1;
        res.push(val);
    }
    res
}

fn part2(input: &Input) -> u64 {
    let input = extend_input(input);
    let ring = play(&input, 10_000_000);
    let a = ring.get_next(1).unwrap();
    let b = ring.get_next(a).unwrap();
    a as u64 * b as u64
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part1, part2)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "389125467";

    #[test]
    fn example_1_part1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(labels(&play(&input, 10)), "92658374");
    }

    #[test]
    fn example_2_part1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part1(&input), "67384529");
    }

    #[test]
    fn example_1_part2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part2(&input), 149245887792);
    }
}
