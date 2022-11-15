use crate::input::*;

struct Ship {
    dir: Dir,
    east: isize,
    north: isize,
}

impl Ship {
    fn navigate(&self, instr: &Instr) -> Ship {
        match instr {
            ('N', i) => self.move_north(*i),
            ('S', i) => self.move_north(-*i),
            ('E', i) => self.move_east(*i),
            ('W', i) => self.move_east(-*i),
            ('L', i) => self.turn(360 - *i),
            ('R', i) => self.turn(*i),
            ('F', i) => self.forward(*i),
            (c, i) => panic!("invalid instruction: {}{}", c, i),
        }
    }

    fn move_north(&self, amount: isize) -> Ship {
        Ship {
            north: self.north + amount,
            ..*self
        }
    }

    fn move_east(&self, amount: isize) -> Ship {
        Ship {
            east: self.east + amount,
            ..*self
        }
    }

    fn turn(&self, degrees: isize) -> Ship {
        let dir = match (self.dir, degrees) {
            (Dir::North, 90) => Dir::East,
            (Dir::North, 180) => Dir::South,
            (Dir::North, 270) => Dir::West,
            (Dir::East, 90) => Dir::South,
            (Dir::East, 180) => Dir::West,
            (Dir::East, 270) => Dir::North,
            (Dir::South, 90) => Dir::West,
            (Dir::South, 180) => Dir::North,
            (Dir::South, 270) => Dir::East,
            (Dir::West, 90) => Dir::North,
            (Dir::West, 180) => Dir::East,
            (Dir::West, 270) => Dir::South,
            _ => panic!("invalid degrees for turn: {}", degrees),
        };
        Ship { dir, ..*self }
    }

    fn forward(&self, amount: isize) -> Ship {
        match self.dir {
            Dir::North => self.move_north(amount),
            Dir::South => self.move_north(-amount),
            Dir::East => self.move_east(amount),
            Dir::West => self.move_east(-amount),
        }
    }
}

pub fn part1(input: &Input) -> usize {
    let ship = Ship {
        dir: Dir::East,
        east: 0,
        north: 0,
    };
    let ship = input.iter().fold(ship, |ship, instr| ship.navigate(instr));
    (ship.east.abs() + ship.north.abs()) as usize
}
