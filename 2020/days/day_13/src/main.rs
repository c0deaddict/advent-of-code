use lib::run;
use std::fmt::Debug;

#[derive(Debug)]
struct Input {
    earliest_ts: usize,
    busses: Vec<(usize, usize)>,
}

fn parse_busses(line: &str) -> Input {
    let busses = line
        .trim()
        .split(',')
        .enumerate()
        .filter_map(|(pos, id)| {
            if id == "x" {
                None
            } else {
                Some((pos, id.parse::<usize>().unwrap()))
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
        for (_, bus) in input.busses.iter() {
            if ts % bus == 0 {
                return i * bus;
            }
        }
    }

    panic!("not found!");
}

// compute: ax + by = gcd(a, b)
// returns: (d = gcd(a, b), x, y)
// source: https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
fn gcd_extended(a: isize, b: isize) -> (isize, isize, isize) {
    if a == 0 {
        (b, 0, 1)
    } else {
        let (d, x1, y1) = gcd_extended(b % a, a);
        let x = y1 - (b / a) * x1;
        let y = x1;
        (d, x, y)
    }
}

// source: https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
fn mod_inverse(a: isize, m: isize) -> Option<isize> {
    let (d, x, _) = gcd_extended(a, m);
    if d != 1 {
        None
    } else {
        // m is added to handle negative x.
        Some((x % m + m) % m)
    }
}

// Use the Chinese Remainder Theorem to solve the set of equations:
//
//   timestamp   = 0 (mod id0)
//   timestamp+1 = 0 (mod id1)
//   ...
//   timestamp+N = 0 (mod idN)
//
// These equations can be rewritten to:
//
//   timestamp = 0 (mod id0)
//   timestamp = id1 - 1 (mod id1)
//   ...
//   timestamp = idN - N (mod idN)
//
// source: http://www-math.ucdenver.edu/~wcherowi/courses/m5410/crt.pdf
//
fn part2(input: &Input) -> usize {
    let m_all: usize = input.busses.iter().map(|(_, id)| id).product();
    let x: usize = input
        .busses
        .iter()
        .map(|(offset, id)| {
            let a_i = id - (offset % id);
            let m_i = m_all / id;
            let y_i = mod_inverse(m_i as isize, *id as isize).unwrap() as usize;
            a_i * m_i * y_i
        })
        .sum();
    x % m_all
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
