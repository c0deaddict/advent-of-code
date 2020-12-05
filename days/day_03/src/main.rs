use lib::run;
use std::collections::HashMap;

struct Trees {
    map: HashMap<(usize, usize), bool>,
    width: usize,
    height: usize,
}

type Path = Vec<(usize, usize)>;

fn parse_input(input: &str) -> Trees {
    let lines = input.lines().map(|l| l.trim()).filter(|l| !l.is_empty());

    let height = lines.clone().count();
    let width = lines.clone().next().unwrap().chars().count();

    let map = lines
        .enumerate()
        .flat_map(|(y, l)| {
            l.chars()
                .map(|c| c == '#')
                .enumerate()
                .map(move |(x, c)| ((y, x), c))
        })
        .collect();

    Trees { map, width, height }
}

fn slope_path(height: usize, right: usize, down: usize) -> Vec<(usize, usize)> {
    (0..(height / down))
        .map(|i| (i * down, i * right))
        .collect()
}

fn count_on_path(trees: &Trees, path: &Path) -> usize {
    path.iter()
        .map(|(y, x)| {
            let vx = x % trees.width;
            match trees.map.get(&(*y, vx)).unwrap() {
                true => 1,
                false => 0,
            }
        })
        .sum()
}

fn part_01(trees: &Trees) -> usize {
    let path = slope_path(trees.height, 3, 1);
    count_on_path(trees, &path)
}

fn part_02(trees: &Trees) -> usize {
    vec![(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        .iter()
        .map(move |(r, d)| slope_path(trees.height, *r, *d))
        .map(|path| count_on_path(trees, &path))
        .fold(1, |res, val| res * val)
}

fn main() {
    run(
        1,
        include_str!("input.txt"),
        parse_input,
        part_01,
        part_02,
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    ..##.......
    #...#...#..
    .#....#..#.
    ..#.#...#.#
    .#...##..#.
    ..#.##.....
    .#.#.#....#
    .#........#
    #.##...#...
    #...##....#
    .#..#...#.#";

    #[test]
    fn test_parse_input() {
        let trees = parse_input(EXAMPLE_DATA_1);
        assert_eq!(trees.height, 11);
        assert_eq!(trees.width, 11);
        assert_eq!(*trees.map.get(&(0, 0)).unwrap(), false);
        assert_eq!(*trees.map.get(&(10, 10)).unwrap(), true);
    }

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 7);
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 336);
    }
}
