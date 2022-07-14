use lib::run;

type Input<'a> = &'a str;

fn parse_input(input: &str) -> Input {
    input
}

fn part_01(input: &Input) -> i32 {
    input.chars().fold(0, |acc, ch| {
        acc + match ch {
            '(' => 1,
            ')' => -1,
            _ => 0,
        }
    })
}

fn part_02(input: &Input) -> i32 {
    let mut floor = 0;
    for (pos, ch) in input.chars().enumerate() {
        floor += match ch {
            '(' => 1,
            ')' => -1,
            _ => 0,
        };
        if floor < 0 {
            return pos as i32 + 1;
        }
    }

    panic!("never went into basement")
}

fn main() {
    run(1, include_str!("../../../../input/day_1.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn examples_part_1() {
        assert_eq!(part_01(&"(())"), 0);
        assert_eq!(part_01(&"()()"), 0);
        assert_eq!(part_01(&"))((((("), 3);
    }

    #[test]
    fn examples_part_2() {
        assert_eq!(part_02(&")"), 1);
        assert_eq!(part_02(&"()())"), 5);
    }
}
