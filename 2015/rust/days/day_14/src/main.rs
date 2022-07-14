use lib::run;
use regex::Regex;

struct Reindeer<'a> {
    name: &'a str,
    speed: usize,
    fly_time: usize,
    rest_time: usize,
}

type Input<'a> = Vec<Reindeer<'a>>;

fn parse_input(input: &str) -> Input {
    let re = Regex::new(
        r"^(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.$",
    )
    .unwrap();

    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| {
            let c = re.captures(l).unwrap();
            let name = c.get(1).unwrap().as_str();
            let speed = c.get(2).unwrap().as_str().parse().unwrap();
            let fly_time = c.get(3).unwrap().as_str().parse().unwrap();
            let rest_time = c.get(4).unwrap().as_str().parse().unwrap();
            Reindeer {
                name,
                speed,
                fly_time,
                rest_time,
            }
        })
        .collect()
}

fn compute_distance(r: &Reindeer, time: usize) -> usize {
    let cycle_time = r.fly_time + r.rest_time;
    let full_cycles = time / cycle_time;
    let mut flying = full_cycles * r.fly_time;
    let current_cycle = time % cycle_time;
    flying += std::cmp::min(current_cycle, r.fly_time);
    flying * r.speed
}

fn max_distance(input: &Input, time: usize) -> usize {
    input
        .iter()
        .map(|r| compute_distance(r, time))
        .max()
        .unwrap()
}

fn part_01(input: &Input) -> usize {
    max_distance(input, 2503)
}

fn max_points(input: &Input, time: usize) -> usize {
    let mut points = vec![0; input.len()];
    for t in 0..time {
        let distances: Vec<_> = input.iter().map(|r| compute_distance(r, t + 1)).collect();
        let max = distances.iter().max().unwrap();
        for (i, d) in distances.iter().enumerate() {
            if d == max {
                points[i] += 1;
            }
        }
    }

    *points.iter().max().unwrap()
}

fn part_02(input: &Input) -> usize {
    max_points(input, 2503)
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
    Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(max_distance(&input, 1000), 1120)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(max_points(&input, 1000), 689)
    }
}
