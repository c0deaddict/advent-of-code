use itertools::Itertools;
use lib::run;

type Input<'a> = &'a str;

fn parse_input(input: &str) -> Input {
    input.trim()
}

fn look_and_say(s: &str) -> String {
    s.chars()
        .group_by(|e| *e)
        .into_iter()
        .map(|(key, group)| format!("{}{}", group.count(), key))
        .collect()
}

fn iterate(s: &str, times: usize) -> usize {
    (0..times)
        .fold((*s).to_owned(), |s, _| look_and_say(&s))
        .len()
}

fn part_01(input: &Input) -> usize {
    iterate(input, 40)
}

fn part_02(input: &Input) -> usize {
    iterate(input, 50)
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn examples_part_1() {
        assert_eq!(look_and_say("1"), "11");
        assert_eq!(look_and_say("11"), "21");
        assert_eq!(look_and_say("21"), "1211");
        assert_eq!(look_and_say("1211"), "111221");
        assert_eq!(look_and_say("111221"), "312211");
    }
}
