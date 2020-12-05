use lib::run;
use std::collections::HashSet;

type Input<'r> = Vec<&'r str>;

fn parse_input<'r>(input: &'r str) -> Input<'r> {
    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .collect()
}

fn seat_id(boarding_pass: &str) -> usize {
    let bin_str = boarding_pass
        .replace(&['F', 'L'][..], "0")
        .replace(&['B', 'R'][..], "1");
    usize::from_str_radix(&bin_str, 2).unwrap()
}

fn part_01(input: &Input) -> usize {
    input.iter().map(|bp| seat_id(&bp)).max().unwrap()
}

fn part_02(input: &Input) -> usize {
    let booked_seats: HashSet<usize> = input.iter().map(|bp| seat_id(&bp)).collect();
    let all_seats: HashSet<usize> = (0..1024).collect();

    *all_seats
        .difference(&booked_seats)
        .find(|seat_id| {
            booked_seats.contains(&(*seat_id + 1)) && booked_seats.contains(&(*seat_id - 1))
        })
        .unwrap()
}

fn main() {
    run(
        1,
        include_str!("input.txt"),
        parse_input,
        part_01,
        part_02,
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example_seat_ids() {
        assert_eq!(seat_id("FBFBBFFRLR"), 357);
        assert_eq!(seat_id("BFFFBBFRRR"), 567);
        assert_eq!(seat_id("FFFBBBFRRR"), 119);
        assert_eq!(seat_id("BBFFBBFRLL"), 820);
    }
}
