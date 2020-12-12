#[derive(Copy, Clone)]
pub enum Dir {
    North,
    South,
    East,
    West,
}

pub type Instr = (char, isize);
pub type Input = Vec<Instr>;

pub fn parse_input(input: &str) -> Input {
    input
        .trim()
        .lines()
        .map(|line| {
            let (d, i) = line.trim().split_at(1);
            (d.chars().next().unwrap(), i.parse::<isize>().unwrap())
        })
        .collect()
}
