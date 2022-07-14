use lib::run;
use md5;

type Input<'a> = &'a str;

fn parse_input(input: &str) -> Input {
    input.trim()
}

fn part_01(input: &Input) -> usize {
    for i in 1.. {
        let key = format!("{}{}", input, i);
        let hash = md5::compute(key);
        if hash[0] == 0 && hash[1] == 0 && hash[2] <= 0x10 {
            return i;
        }
    }

    panic!("unreachable");
}

fn part_02(input: &Input) -> usize {
    for i in 1.. {
        let key = format!("{}{}", input, i);
        let hash = md5::compute(key);
        if hash[0] == 0 && hash[1] == 0 && hash[2] == 0 {
            return i;
        }
    }

    panic!("unreachable");
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example1_part_1() {
        assert_eq!(part_01(&"abcdef"), 609043)
    }

    #[test]
    fn example2_part_1() {
        assert_eq!(part_01(&"pqrstuv"), 1048970)
    }
}
