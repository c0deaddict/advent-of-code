use crate::input::*;
use crate::part1::solve_puzzle;
use crate::types::*;

const SEA_MONSTER: &'static str = "
------------------#-
#----##----##----###
-#--#--#--#--#--#---";

fn assemble_image(puzzle: Vec<Tile>, size: usize) -> Image {
    let mut image = Image::new(8 * size);
    for ty in 0..size {
        for tx in 0..size {
            for y in 1..9 {
                for x in 1..9 {
                    let tile = &puzzle[ty * size + tx];
                    let v = tile.image.get(y, x);
                    image.set(ty * 8 + y - 1, tx * 8 + x - 1, v);
                }
            }
        }
    }
    image
}

fn parse_sea_monster() -> Vec<Vec<bool>> {
    SEA_MONSTER
        .trim()
        .lines()
        .map(|line| line.trim().chars().map(|ch| ch == '#').collect())
        .collect()
}

fn monster_size(monster: &Vec<Vec<bool>>) -> usize {
    monster
        .iter()
        .map(|line| line.iter().filter(|x| **x).count())
        .sum()
}

fn count_monsters(monster: &Vec<Vec<bool>>, image: &Image) -> usize {
    let mheight = monster.len();
    let mwidth = monster[0].len();
    let mut count = 0;

    for sy in 0..(image.size - mheight) {
        'search: for sx in 0..(image.size - mwidth) {
            for y in 0..mheight {
                for x in 0..mwidth {
                    if monster[y][x] && !image.get(sy + y, sx + x) {
                        continue 'search;
                    }
                }
            }

            count += 1;
        }
    }

    count
}

fn print_puzzle(puzzle: &Vec<Tile>, size: usize) {
    for ty in 0..size {
        for y in 0..10 {
            let line = (0..size)
                .map(|tx| {
                    let tile = &puzzle[ty * size + tx];
                    (0..10)
                        .map(|x| if tile.image.get(y, x) { '#' } else { '.' })
                        .collect()
                })
                .collect::<Vec<String>>()
                .join("  ");
            println!("{}", line);
        }
        println!("");
    }
}

fn print_image(image: &Image) {
    for y in 0..image.size {
        let line: String = (0..image.size)
            .map(|x| if image.get(y, x) { '#' } else { '.' })
            .collect();
        println!("{}", line);
    }
}

pub fn part2(input: &Input) -> usize {
    let (puzzle, size) = solve_puzzle(input);
    print_puzzle(&puzzle, size);
    println!("");

    let image = assemble_image(puzzle, size);
    print_image(&image);
    println!("");
    let monster = parse_sea_monster();

    image
        .configs()
        .iter()
        .filter_map(|image| {
            let count = count_monsters(&monster, &image);
            if count > 0 {
                let mut roughness = image.count();
                roughness -= count * monster_size(&monster);
                Some(roughness)
            } else {
                None
            }
        })
        .next()
        .unwrap()
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = include_str!("example_1.txt");

    #[test]
    fn example_1_part2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part2(&input), 273);
    }
}
