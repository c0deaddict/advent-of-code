use itertools::Itertools;
use lazy_static::lazy_static;
use lib::run;

type Entry<'a> = (Vec<&'a str>, Vec<&'a str>);
type Input<'a> = Vec<Entry<'a>>;

fn parse_input(input: &str) -> Input {
    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| {
            let (digits, output) = l.split(" | ").collect_tuple().unwrap();
            (
                digits.split_whitespace().collect(),
                output.split_whitespace().collect(),
            )
        })
        .collect()
}

fn part_01(input: &Input) -> usize {
    input
        .iter()
        .flat_map(|(_, output)| output)
        .map(|s| match s.len() {
            2 | 4 | 3 | 7 => 1,
            _ => 0,
        })
        .sum()
}

lazy_static! {
    static ref SEGMENTS: Vec<&'static str> = vec![
        "abcefg", "cf", "acdeg", "acdfg", "bcdf", "abdfg", "abdefg", "acf", "abcdefg", "abcdfg",
    ];
}

fn map_digit(digit: &str, order: &Vec<char>) -> String {
    digit
        .chars()
        .map(|c| order[((c as u8) - ('a' as u8)) as usize])
        .sorted()
        .collect()
}

fn valid_order(entry: &Entry, order: &Vec<char>) -> bool {
    for digit in &entry.0 {
        let mapped = map_digit(digit, order);
        if !SEGMENTS.contains(&mapped.as_str()) {
            return false;
        }
    }
    return true;
}

fn deduce_digits(entry: &Entry) -> usize {
    for order in "abcdefg".chars().permutations(7) {
        if valid_order(entry, &order) {
            let number: String = entry
                .1
                .iter()
                .map(|digit| {
                    let mapped = map_digit(digit, &order);
                    let (num, _) = SEGMENTS
                        .iter()
                        .find_position(|segment| *segment == &mapped.as_str())
                        .unwrap();
                    num.to_string()
                })
                .collect();
            return number.parse().unwrap();
        }
    }

    panic!("no match");
}

fn part_02(input: &Input) -> usize {
    input.iter().map(deduce_digits).sum()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
    edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
    fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
    fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
    aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
    fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
    dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
    bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
    egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
    gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 26)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 61229)
    }
}
