use lib::run;
use std::fmt::Debug;

#[derive(Debug)]
struct Input {
    earliest_ts: usize,
    busses: Vec<Option<usize>>,
}

fn parse_busses(line: &str) -> Input {
    let busses = line
        .trim()
        .split(',')
        .map(|id| {
            if id == "x" {
                None
            } else {
                Some(id.parse::<usize>().unwrap())
            }
        })
        .collect();

    Input {
        earliest_ts: 0,
        busses,
    }
}

fn parse_input(input: &str) -> Input {
    let mut lines = input.trim().lines();
    let earliest_ts = lines.next().unwrap().trim().parse::<usize>().unwrap();
    let result = parse_busses(lines.next().unwrap());
    Input {
        earliest_ts,
        ..result
    }
}

fn part1(input: &Input) -> usize {
    for i in 0.. {
        let ts = input.earliest_ts + i;
        for bus in input.busses.iter() {
            if let Some(bus) = bus {
                if ts % bus == 0 {
                    return i * bus;
                }
            }
        }
    }

    panic!("not found!");
}

fn part2(input: &Input) -> usize {
    let (offset, max_step) = input
        .busses
        .iter()
        .enumerate()
        .max_by(|(_, a), (_, b)| a.cmp(b))
        .unwrap();

    let max_step = max_step.unwrap();

    'outer: for i in (max_step..).step_by(max_step) {
        if i % 10000000 == 0 {
            println!("{}", i);
        }
        for (j, bus) in input.busses.iter().enumerate() {
            if let Some(bus) = bus {
                if (i + j - offset) % bus != 0 {
                    continue 'outer;
                }
            }
        }
        return i - offset;
    }

    panic!("not found!");
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part1, part2)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    939
    7,13,x,x,59,x,31,19";

    #[test]
    fn example_1_part1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part1(&input), 295);
    }

    #[test]
    fn example_1_part2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part2(&input), 1068781);
    }

    #[test]
    fn example_2_part2() {
        let input = parse_busses("17,x,13,19");
        assert_eq!(part2(&input), 3417);
    }

    #[test]
    fn example_3_part2() {
        let input = parse_busses("67,7,59,61");
        assert_eq!(part2(&input), 754018);
    }

    #[test]
    fn example_4_part2() {
        let input = parse_busses("67,x,7,59,61");
        assert_eq!(part2(&input), 779210);
    }

    #[test]
    fn example_5_part2() {
        let input = parse_busses("67,7,x,59,61");
        assert_eq!(part2(&input), 1261476);
    }

    #[test]
    fn example_6_part2() {
        let input = parse_busses("1789,37,47,1889");
        assert_eq!(part2(&input), 1202161486);
    }
}
