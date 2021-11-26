use lib::run;
use regex::Regex;
use std::collections::HashSet;

type Input = Vec<Vec<String>>;
type Pos = (isize, isize);
type Tiles = HashSet<Pos>;

fn parse_input(input: &str) -> Input {
    let re = Regex::new(r"e|se|sw|w|nw|ne").unwrap();

    input
        .trim()
        .lines()
        .map(|line| {
            re.captures_iter(line.trim())
                .map(|c| c[0].to_owned())
                .collect()
        })
        .collect()
}

fn follow_path(path: &Vec<String>) -> Pos {
    let mut x = 0;
    let mut y = 0;
    for step in path {
        match &step[..] {
            "e" => x += 2,
            "se" => {
                x += 1;
                y -= 1;
            }
            "sw" => {
                x -= 1;
                y -= 1;
            }
            "w" => x -= 2,
            "nw" => {
                x -= 1;
                y += 1;
            }
            "ne" => {
                x += 1;
                y += 1;
            }
            _ => panic!("unexpected pattern {}", step),
        }
    }
    (x, y)
}

fn flip_tiles(input: &Input) -> Tiles {
    let mut black = HashSet::new();
    for path in input {
        let tile = follow_path(path);
        if !black.insert(tile) {
            black.remove(&tile);
        }
    }
    black
}

fn part1(input: &Input) -> usize {
    flip_tiles(input).len()
}

fn neighbours(pos: &Pos) -> Vec<Pos> {
    let (x, y) = *pos;
    vec![
        (x + 2, y),     // e
        (x + 1, y - 1), // se
        (x - 1, y - 1), // sw
        (x - 2, y),     // w
        (x - 1, y + 1), // nw
        (x + 1, y + 1), // ne
    ]
}

fn count_neighbours(pos: &Pos, tiles: &Tiles) -> usize {
    neighbours(pos).iter().filter(|p| tiles.contains(p)).count()
}

fn flip_step(input_black: Tiles) -> Tiles {
    let mut new_black = HashSet::new();
    let mut new_white = HashSet::new();

    for pos in input_black.iter() {
        // Count the black neighbours.
        let black_count = count_neighbours(pos, &input_black);
        if black_count == 0 || black_count > 2 {
            new_white.insert(*pos);
        } else {
            new_black.insert(*pos);
        }

        // Visit the white neighbours.
        for pos in neighbours(pos).iter() {
            if input_black.contains(pos) || new_white.contains(pos) || new_black.contains(pos) {
                continue;
            }

            let black_count = count_neighbours(pos, &input_black);
            if black_count == 2 {
                new_black.insert(*pos);
            } else {
                new_white.insert(*pos);
            }
        }
    }

    new_black
}

fn part2(input: &Input) -> usize {
    let mut black = flip_tiles(input);
    for _ in 0..100 {
        black = flip_step(black);
    }
    black.len()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part1, part2)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    sesenwnenenewseeswwswswwnenewsewsw
    neeenesenwnwwswnenewnwwsewnenwseswesw
    seswneswswsenwwnwse
    nwnwneseeswswnenewneswwnewseswneseene
    swweswneswnenwsewnwneneseenw
    eesenwseswswnenwswnwnwsewwnwsene
    sewnenenenesenwsewnenwwwse
    wenwwweseeeweswwwnwwe
    wsweesenenewnwwnwsenewsenwwsesesenwne
    neeswseenwwswnwswswnw
    nenwswwsewswnenenewsenwsenwnesesenew
    enewnwewneswsewnwswenweswnenwsenwsw
    sweneswneswneneenwnewenewwneswswnese
    swwesenesewenwneswnwwneseswwne
    enesenwswwswneneswsenwnewswseenwsese
    wnwnesenesenenwwnenwsewesewsesesew
    nenewswnwewswnenesenwnesewesw
    eneswnwswnwsenenwnwnwwseeswneewsenese
    neswnwewnwnwseenwseesewsenwsweewe
    wseweeenwnesenwwwswnew";

    #[test]
    fn example_1_part1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part1(&input), 10);
    }

    #[test]
    fn example_1_part2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part2(&input), 2208);
    }
}
