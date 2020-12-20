use day_20::types::*;
use itertools::Itertools;
use lib::run;
use regex::Regex;
use std::collections::{HashMap, HashSet};

type Input = Vec<Tile>;
type Puzzle<'a> = Vec<&'a Tile>;
type AdjMap<'a> = HashMap<&'a Tile, HashSet<&'a Tile>>;

fn parse_input(input: &str) -> Input {
    let header_re = Regex::new(r"^Tile (\d+):$").unwrap();

    input
        .trim()
        .split("\n\n")
        .map(|tile| {
            let mut it = tile.lines();
            let header = it.next().unwrap().trim();
            let id = header_re.captures(header).unwrap()[1].parse().unwrap();
            let mut image = [[false; 10]; 10];
            for (y, line) in it.enumerate() {
                for (x, ch) in line.chars().enumerate() {
                    image[y][x] = ch == '#';
                }
            }

            Tile::new(id, image)
        })
        .collect()
}

// Calculate which tiles can be adjacent to each other.
fn adjacent_tiles<'a>(configs: &'a Vec<Tile>, horz: bool) -> AdjMap<'a> {
    configs
        .iter()
        .flat_map(|t| if horz { t.hborders() } else { t.vborders() })
        .fold(HashMap::new(), |mut map, (k, v)| {
            map.entry(k).or_insert_with(|| Vec::new()).push(v);
            map
        })
        .iter()
        .flat_map(|(_, sides)| {
            sides
                .iter()
                .cartesian_product(sides.iter())
                .filter_map(|((ta, sa), (tb, sb))| {
                    if ta.id == tb.id {
                        None
                    } else if horz && *sa == Side::Bottom && *sb == Side::Top {
                        Some((*ta, *tb))
                    } else if !horz && *sa == Side::Right && *sb == Side::Left {
                        Some((*ta, *tb))
                    } else {
                        None
                    }
                })
        })
        .fold(HashMap::new(), |mut map, (k, v)| {
            map.entry(k).or_insert_with(|| HashSet::new()).insert(v);
            map
        })
}

fn search<'a>(
    puzzle: Puzzle<'a>,
    size: usize,
    hadj: &'a AdjMap,
    vadj: &'a AdjMap,
) -> Option<Puzzle<'a>> {
    let i = puzzle.len();
    if i == size * size {
        return Some(puzzle);
    }

    let y = i / size;
    let x = i % size;

    let h = if x > 0 { hadj.get(puzzle[i - 1]) } else { None };

    let v = if y > 0 {
        vadj.get(puzzle[x + (y - 1) * size])
    } else {
        None
    };

    let options = match (h, v) {
        (Some(h), None) => h.to_owned(),
        (None, Some(v)) => v.to_owned(),
        (Some(h), Some(v)) => h & v,
        (None, None) => HashSet::new(),
    };

    for tile in options {
        // Ignore tiles that are already used.
        if puzzle.iter().any(|t| t.id == tile.id) {
            continue;
        }

        let mut new_puzzle = puzzle.clone();
        new_puzzle.push(tile);

        if let Some(result) = search(new_puzzle, size, hadj, vadj) {
            return Some(result);
        }
    }

    None
}

fn corners<'a>(puzzle: Puzzle<'a>, size: usize) -> Vec<&'a Tile> {
    vec![
        puzzle[0],
        puzzle[size - 1],
        puzzle[size * (size - 1)],
        puzzle[(size * size) - 1],
    ]
}

fn part1(input: &Input) -> usize {
    // Image is square.
    let size = (input.len() as f64).sqrt() as usize;

    let configs: Vec<Tile> = input.iter().flat_map(|t| t.configs()).collect();
    let hadj = adjacent_tiles(&configs, true);
    let vadj = adjacent_tiles(&configs, false);

    // Try each tile as initial.
    let puzzle = configs
        .iter()
        .filter_map(|tile| {
            let mut puzzle = Vec::with_capacity(size * size);
            puzzle.push(tile);
            search(puzzle, size, &hadj, &vadj)
        })
        .next()
        .unwrap();

    corners(puzzle, size).iter().map(|t| t.id).product()
}

fn part2(_input: &Input) -> usize {
    0
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part1, part2)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = include_str!("example_1.txt");

    #[test]
    fn example_1_part1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part1(&input), 20899048083289);
    }
}
