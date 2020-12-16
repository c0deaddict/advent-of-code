use itertools::Itertools;
use lib::run;
use regex::Regex;
use std::collections::HashSet;
use std::fmt::Debug;

#[derive(Debug)]
struct Range {
    low: u64,
    high: u64,
}

impl Range {
    fn new(low: u64, high: u64) -> Range {
        Range { low, high }
    }

    fn contains(&self, value: u64) -> bool {
        value >= self.low && value <= self.high
    }
}

#[derive(Debug)]
struct Validation {
    name: String,
    ranges: Vec<Range>,
}

impl Validation {
    fn matches(&self, value: u64) -> bool {
        self.ranges.iter().any(|range| range.contains(value))
    }
}

#[derive(Debug)]
struct Input {
    validations: Vec<Validation>,
    your_ticket: Vec<u64>,
    nearby_tickets: Vec<Vec<u64>>,
}

fn parse_input(input: &str) -> Input {
    let re = Regex::new(r"^([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)$").unwrap();

    let (validations, your_ticket, nearby_tickets) =
        input.trim().split("\n\n").collect_tuple().unwrap();

    let validations = validations
        .trim()
        .lines()
        .map(|line| {
            let c = re.captures(line.trim()).unwrap();
            let name = c[1].to_owned();
            let ranges = vec![
                Range::new(c[2].parse().unwrap(), c[3].parse().unwrap()),
                Range::new(c[4].parse().unwrap(), c[5].parse().unwrap()),
            ];
            Validation { name, ranges }
        })
        .collect();

    let your_ticket = your_ticket
        .trim()
        .lines()
        .skip(1)
        .next()
        .unwrap()
        .trim()
        .split(',')
        .map(|s| s.parse().unwrap())
        .collect();

    let nearby_tickets = nearby_tickets
        .trim()
        .lines()
        .skip(1)
        .map(|line| line.trim().split(',').map(|s| s.parse().unwrap()).collect())
        .collect();

    Input {
        validations,
        your_ticket,
        nearby_tickets,
    }
}

fn valid_for_any_field(input: &Input, value: &u64) -> bool {
    input.validations.iter().any(|rule| rule.matches(*value))
}

fn part1(input: &Input) -> u64 {
    input
        .nearby_tickets
        .iter()
        .flat_map(|ticket| {
            ticket
                .iter()
                .filter(|value| !valid_for_any_field(input, value))
        })
        .sum()
}

fn valid_tickets(input: &Input) -> Vec<Vec<u64>> {
    input
        .nearby_tickets
        .iter()
        .cloned()
        .filter(|ticket| ticket.iter().all(|value| valid_for_any_field(input, value)))
        .collect()
}

fn determine_mapping<'r>(input: &'r Input) -> Vec<&'r str> {
    let options: Vec<Vec<HashSet<&str>>> = valid_tickets(input)
        .iter()
        .map(|ticket| {
            ticket
                .iter()
                .map(|value| {
                    input
                        .validations
                        .iter()
                        .filter(|rule| rule.matches(*value))
                        .map(|rule| &rule.name[..])
                        .collect()
                })
                .collect()
        })
        .collect();

    let mut it = options.iter();
    let first_row: Vec<HashSet<&str>> = it.next().unwrap().iter().cloned().collect();
    let mut undetermined_fields = it.fold(first_row, |res, row| {
        res.iter().zip(row).map(|(a, b)| a & b).collect()
    });
    let mut mapping = vec![None; undetermined_fields.len()];

    loop {
        let candidate = undetermined_fields
            .iter()
            .cloned()
            .find_position(|f| f.len() == 1)
            .map(|(i, field_set)| (i, field_set.iter().cloned().next().unwrap()));

        if let Some((i, field)) = candidate {
            mapping[i] = Some(field);

            for field_set in undetermined_fields.iter_mut() {
                field_set.remove(field);
            }
        } else {
            break;
        }
    }

    mapping.iter().map(|f| f.unwrap()).collect()
}

fn part2(input: &Input) -> u64 {
    determine_mapping(input)
        .iter()
        .enumerate()
        .filter(|(_, f)| f.starts_with("departure"))
        .map(|(i, _)| input.your_ticket[i])
        .product()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part1, part2)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    class: 1-3 or 5-7
    row: 6-11 or 33-44
    seat: 13-40 or 45-50

    your ticket:
    7,1,14

    nearby tickets:
    7,3,47
    40,4,50
    55,2,20
    38,6,12";

    #[test]
    fn example_1_part1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part1(&input), 71);
    }

    const EXAMPLE_DATA_2: &'static str = "
    class: 0-1 or 4-19
    row: 0-5 or 8-19
    seat: 0-13 or 16-19

    your ticket:
    11,12,13

    nearby tickets:
    3,9,18
    15,1,5
    5,14,9";

    #[test]
    fn example_1_part2() {
        let input = parse_input(EXAMPLE_DATA_2);
        assert_eq!(determine_mapping(&input), vec!["row", "class", "seat"]);
    }
}
