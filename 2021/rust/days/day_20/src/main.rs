use itertools::Itertools;
use lib::run;
use std::collections::HashSet;

#[derive(Debug, Hash, Eq, PartialEq, Copy, Clone)]
struct Position {
    x: i32,
    y: i32,
}

type Bitmap = Vec<bool>;

#[derive(Clone)]
struct Bounds {
    min: Position,
    max: Position,
}

#[derive(Clone)]
struct Image {
    set: HashSet<Position>,
    bounds: Bounds,
    default: bool,
}

struct Input {
    bitmap: Bitmap,
    image: Image,
}

fn parse_input(input: &str) -> Input {
    let (bitmap, set) = input.trim().splitn(2, "\n\n").collect_tuple().unwrap();

    let bitmap: Vec<_> = bitmap.trim().chars().map(|c| c == '#').collect();

    let set = set
        .trim()
        .lines()
        .enumerate()
        .flat_map(|(y, l)| {
            l.trim()
                .chars()
                .enumerate()
                .filter_map(|(x, ch)| {
                    if ch == '#' {
                        Some(Position {
                            x: x as i32,
                            y: y as i32,
                        })
                    } else {
                        None
                    }
                })
                .collect::<Vec<_>>()
        })
        .collect();

    let image = Image::new(set, false);
    Input { bitmap, image }
}

impl Position {
    fn in_bounds(&self, bounds: &Bounds) -> bool {
        self.x >= bounds.min.x
            && self.x <= bounds.max.x
            && self.y >= bounds.min.y
            && self.y <= bounds.max.y
    }
}

impl Image {
    fn new(set: HashSet<Position>, default: bool) -> Image {
        let min = Position {
            x: set.iter().min_by_key(|p| p.x).unwrap().x,
            y: set.iter().min_by_key(|p| p.y).unwrap().y,
        };
        let max = Position {
            x: set.iter().max_by_key(|p| p.x).unwrap().x,
            y: set.iter().max_by_key(|p| p.y).unwrap().y,
        };
        let bounds = Bounds { min, max };
        Image {
            set,
            bounds,
            default,
        }
    }

    fn get(&self, pos: &Position) -> bool {
        if pos.in_bounds(&self.bounds) {
            self.set.contains(pos)
        } else {
            self.default
        }
    }

    fn count(&self) -> usize {
        self.set.len()
    }
}

fn step(image: &Image, bitmap: &Bitmap) -> Image {
    let mut res = HashSet::new();
    for y in image.bounds.min.y - 2..=image.bounds.max.y + 2 {
        for x in image.bounds.min.x - 2..=image.bounds.max.x + 2 {
            let mut index = 0;
            for ry in -1..=1 {
                for rx in -1..=1 {
                    let p = Position {
                        x: x + rx,
                        y: y + ry,
                    };
                    index *= 2;
                    if image.get(&p) {
                        index += 1;
                    }
                }
            }
            if bitmap[index] {
                res.insert(Position { x, y });
            }
        }
    }
    let default = if image.default {
        bitmap[511]
    } else {
        bitmap[0]
    };
    let image = Image::new(res, default);
    // print(&image);
    return image;
}

fn print(image: &Image) {
    for y in image.bounds.min.y - 2..=image.bounds.max.y + 2 {
        for x in image.bounds.min.x - 2..=image.bounds.max.x + 2 {
            if image.get(&Position { x, y }) {
                print!("#");
            } else {
                print!(".");
            }
        }
        println!("");
    }
    println!("");
}

fn enhance(input: &Input, steps: usize) -> Image {
    (0..steps).fold(input.image.clone(), |image, _| step(&image, &input.bitmap))
}

fn part_01(input: &Input) -> usize {
    enhance(&input, 2).count()
}

fn part_02(input: &Input) -> usize {
    enhance(&input, 50).count()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = include_str!("example.txt");

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 35)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 3351)
    }
}
