use crate::types::*;

use regex::Regex;

pub type Input = Vec<Tile>;

pub fn parse_input(input: &str) -> Input {
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
