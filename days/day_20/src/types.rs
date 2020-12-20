use std::clone::Clone;
use std::cmp::{Eq, PartialEq};
use std::fmt;
use std::fmt::Debug;
use std::hash::Hash;

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

#[derive(Debug, Clone, Eq, PartialEq, Hash)]
pub struct Image {
    pub size: usize,
    pub data: Vec<bool>,
    pub config: Config,
}

impl Image {
    pub fn new(size: usize) -> Image {
        let config = Config {
            hflip: false,
            vflip: false,
            rotate: Rotate::R0,
        };
        let data = vec![false; size * size];
        Image { size, data, config }
    }

    pub fn get(&self, y: usize, x: usize) -> bool {
        self.data[y * self.size + x]
    }

    pub fn set(&mut self, y: usize, x: usize, v: bool) {
        self.data[y * self.size + x] = v;
    }

    pub fn count(&self) -> usize {
        self.data.iter().filter(|x| **x).count()
    }

    fn new_config(&self, config: Config) -> Image {
        let data = self.data.clone();
        Image {
            config,
            data,
            ..*self
        }
    }

    fn rotate(&self) -> Image {
        let mut res = self.new_config(self.config.rotate());
        for y in 0..self.size {
            for x in 0..self.size {
                res.set(y, x, self.get(x, (self.size - 1) - y));
            }
        }
        res
    }

    fn hflip(&self) -> Image {
        let mut res = self.new_config(self.config.hflip());
        for y in 0..self.size {
            for x in 0..self.size {
                res.set(y, x, self.get((self.size - 1) - y, x));
            }
        }
        res
    }

    fn vflip(&self) -> Image {
        let mut res = self.new_config(self.config.vflip());
        for y in 0..self.size {
            for x in 0..self.size {
                res.set(y, x, self.get(y, (self.size - 1) - x));
            }
        }
        res
    }

    // 8 configs: 16 permutations but 8 are identical.
    pub fn configs(&self) -> Vec<Image> {
        let mut res = vec![];

        res.push(self.clone());
        res.push(self.hflip());
        res.push(self.vflip());

        let r90 = self.rotate();
        res.push(r90.clone());
        res.push(r90.hflip());

        let r180 = r90.rotate();
        res.push(r180.clone());

        let r270 = r180.rotate();
        res.push(r270.clone());
        res.push(r270.hflip());

        res
    }
}

pub type Border = [bool; 10];

#[derive(Debug, Clone, Eq, PartialEq, Hash)]
pub struct Tile {
    pub id: usize,
    pub image: Image,
}

impl fmt::Display for Tile {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}{}", self.id, self.image.config)
    }
}

impl Tile {
    pub fn new(id: usize, image: Image) -> Tile {
        Tile { id, image }
    }

    pub fn configs(&self) -> Vec<Tile> {
        self.image
            .configs()
            .iter()
            .map(|image| Tile {
                image: image.clone(),
                ..*self
            })
            .collect()
    }

    fn border_top(&self) -> Border {
        let mut res = [false; 10];
        for x in 0..10 {
            res[x] = self.image.get(0, x);
        }
        res
    }

    fn border_bottom(&self) -> Border {
        let mut res = [false; 10];
        for x in 0..10 {
            res[x] = self.image.get(9, x);
        }
        res
    }

    fn border_left(&self) -> Border {
        let mut res = [false; 10];
        for y in 0..10 {
            res[y] = self.image.get(y, 0);
        }
        res
    }

    fn border_right(&self) -> Border {
        let mut res = [false; 10];
        for y in 0..10 {
            res[y] = self.image.get(y, 9);
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
