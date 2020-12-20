use std::clone::Clone;
use std::cmp::{Eq, PartialEq};
use std::fmt;
use std::fmt::Debug;
use std::hash::Hash;

pub type Image = [[bool; 10]; 10];
pub type Border = [bool; 10];

#[derive(Debug, Clone, Copy, Eq, PartialEq, Hash)]
pub enum Rotate {
    R0,
    R90,
    R180,
    R270,
}

#[derive(Debug, Clone, Copy, Eq, PartialEq, Hash)]
pub struct Config {
    hflip: bool,
    vflip: bool,
    rotate: Rotate,
}

impl fmt::Display for Config {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let s = match self.rotate {
            Rotate::R0 => "r0",
            Rotate::R90 => "r1",
            Rotate::R180 => "r2",
            Rotate::R270 => "r3",
        };
        let mut s = s.to_owned();
        if self.hflip {
            s += "h";
        }
        if self.vflip {
            s += "v";
        }
        write!(f, "{}", s)
    }
}

impl Config {
    pub fn rotate(&self) -> Config {
        let rotate = match self.rotate {
            Rotate::R0 => Rotate::R90,
            Rotate::R90 => Rotate::R180,
            Rotate::R180 => Rotate::R270,
            Rotate::R270 => Rotate::R0,
        };
        Config { rotate, ..*self }
    }

    pub fn hflip(&self) -> Config {
        Config {
            hflip: !self.hflip,
            ..*self
        }
    }

    pub fn vflip(&self) -> Config {
        Config {
            vflip: !self.vflip,
            ..*self
        }
    }
}

#[derive(Debug, Clone, Copy, Eq, PartialEq, Hash)]
pub enum Side {
    Top,
    Bottom,
    Left,
    Right,
}

#[derive(Debug, Clone, Copy, Eq, PartialEq, Hash)]
pub struct Tile {
    pub id: usize,
    pub image: Image,
    pub config: Config,
}

impl fmt::Display for Tile {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}{}", self.id, self.config)
    }
}

impl Tile {
    pub fn new(id: usize, image: Image) -> Tile {
        let config = Config {
            hflip: false,
            vflip: false,
            rotate: Rotate::R0,
        };
        Tile { id, image, config }
    }

    fn rotate(&self) -> Tile {
        let mut image = [[false; 10]; 10];
        for y in 0..10 {
            for x in 0..10 {
                image[y][x] = self.image[x][9 - y];
            }
        }
        Tile {
            image,
            id: self.id,
            config: self.config.rotate(),
        }
    }

    fn hflip(&self) -> Tile {
        let mut image = [[false; 10]; 10];
        for y in 0..10 {
            for x in 0..10 {
                image[y][x] = self.image[9 - y][x];
            }
        }
        Tile {
            image,
            id: self.id,
            config: self.config.hflip(),
        }
    }

    fn vflip(&self) -> Tile {
        let mut image = [[false; 10]; 10];
        for y in 0..10 {
            for x in 0..10 {
                image[y][x] = self.image[y][9 - x];
            }
        }
        Tile {
            image,
            id: self.id,
            config: self.config.vflip(),
        }
    }

    // 8 configs: 16 permutations but 8 are identical.
    pub fn configs(&self) -> Vec<Tile> {
        let mut res = vec![];

        let tile = *self;
        res.push(tile);
        res.push(tile.hflip());
        res.push(tile.vflip());

        let r90 = tile.rotate();
        res.push(r90);
        res.push(r90.hflip());

        let r180 = r90.rotate();
        res.push(r180);

        let r270 = r180.rotate();
        res.push(r270);
        res.push(r270.hflip());

        res
    }

    fn border_top(&self) -> Border {
        self.image[0]
    }

    fn border_bottom(&self) -> Border {
        self.image[9]
    }

    fn border_left(&self) -> Border {
        let mut res = [false; 10];
        for y in 0..10 {
            res[y] = self.image[y][0];
        }
        res
    }

    fn border_right(&self) -> Border {
        let mut res = [false; 10];
        for y in 0..10 {
            res[y] = self.image[y][9];
        }
        res
    }

    pub fn hborders(&self) -> Vec<(Border, (&Tile, Side))> {
        vec![
            (self.border_top(), (self, Side::Top)),
            (self.border_bottom(), (self, Side::Bottom)),
        ]
    }

    pub fn vborders(&self) -> Vec<(Border, (&Tile, Side))> {
        vec![
            (self.border_left(), (self, Side::Left)),
            (self.border_right(), (self, Side::Right)),
        ]
    }
}
