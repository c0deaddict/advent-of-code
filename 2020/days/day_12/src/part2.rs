use crate::input::*;

struct Ship {
    east: isize,
    north: isize,
    wp_east: isize,
    wp_north: isize,
}

impl Ship {
    fn navigate(&self, instr: &Instr) -> Ship {
        match instr {
            ('N', i) => self.move_wp_north(*i),
            ('S', i) => self.move_wp_north(-*i),
            ('E', i) => self.move_wp_east(*i),
            ('W', i) => self.move_wp_east(-*i),
            ('L', i) => self.rotate_wp(360 - *i),
            ('R', i) => self.rotate_wp(*i),
            ('F', i) => self.forward(*i),
            (c, i) => panic!("invalid instruction: {}{}", c, i),
        }
    }

    fn move_wp_north(&self, amount: isize) -> Ship {
        Ship {
            wp_north: self.wp_north + amount,
            ..*self
        }
    }

    fn move_wp_east(&self, amount: isize) -> Ship {
        Ship {
            wp_east: self.wp_east + amount,
            ..*self
        }
    }

    fn rotate_wp(&self, degrees: isize) -> Ship {
        let (wp_east, wp_north) = match degrees {
            90 => (self.wp_north, -self.wp_east),
            180 => (-self.wp_east, -self.wp_north),
            270 => (-self.wp_north, self.wp_east),
            _ => panic!("invalid rotate degrees {}", degrees),
        };
        Ship {
            wp_east,
            wp_north,
            ..*self
        }
    }

    fn forward(&self, count: isize) -> Ship {
        Ship {
            east: self.east + count * self.wp_east,
            north: self.north + count * self.wp_north,
            ..*self
        }
    }
}

pub fn part2(input: &Input) -> usize {
    let ship = Ship {
        east: 0,
        north: 0,
        wp_east: 10,
        wp_north: 1,
    };
    let ship = input.iter().fold(ship, |ship, instr| ship.navigate(instr));
    (ship.east.abs() + ship.north.abs()) as usize
}
