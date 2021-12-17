use itertools::Itertools;
use lib::run;
use regex::Regex;

#[derive(Debug)]
struct TargetArea {
    x1: i32,
    x2: i32,
    y1: i32,
    y2: i32,
}

type Input = TargetArea;

fn parse_input(input: &str) -> Input {
    let re = Regex::new(r"^target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)$").unwrap();
    let c = re.captures(input.trim()).unwrap();
    let (x1, x2, y1, y2) = c
        .iter()
        .skip(1)
        .map(|s| s.unwrap().as_str().parse().unwrap())
        .collect_tuple()
        .unwrap();
    TargetArea { x1, x2, y1, y2 }
}

/// vx is always positive.
/// target.y1,y2 are always below 0.
fn trajectory(vx: i32, vy: i32, target: &TargetArea) -> Option<i32> {
    let (ox, oy) = (vx, vy);
    let mut vx = vx;
    let mut vy = vy;
    let mut x = 0;
    let mut y = 0;
    let mut maxy = 0;
    loop {
        x += vx;
        y += vy;
        if y > maxy {
            maxy = y;
        }
        vx = if vx == 0 { 0 } else { vx - 1 };
        vy -= 1;
        if x >= target.x1 && x <= target.x2 && y >= target.y1 && y <= target.y2 {
            return Some(maxy);
        } else if x > target.x2 {
            return None;
        } else if vx == 0 && x < target.x1 {
            return None;
        } else if y < target.y1 && vy < 0 {
            return None;
        }
    }
}

fn part_01(input: &Input) -> i32 {
    let maxy = 1000; // empirically determined..
    (2..=input.x2)
        .cartesian_product(input.y1..=maxy)
        .filter_map(|(vx, vy)| trajectory(vx, vy, &input))
        .max()
        .unwrap()
}

fn part_02(input: &Input) -> usize {
    let maxy = 1000; // empirically determined..
    (2..=input.x2)
        .cartesian_product(input.y1..=maxy)
        .filter_map(|(vx, vy)| trajectory(vx, vy, &input))
        .count()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    target area: x=20..30, y=-10..-5
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 45)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 112)
    }    
}
