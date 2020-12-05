use lib::run;

fn parse_input(input: &str) -> Vec<i32> {
    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| l.parse::<i32>().unwrap())
        .collect::<Vec<i32>>()
}

fn part_01(input: &Vec<i32>) -> i32 {
    for (i, a) in input.iter().enumerate() {
        for (j, b) in input.iter().enumerate() {
            if i != j && a + b == 2020 {
                return a * b;
            }
        }
    }

    panic!("failed to find answer");
}

fn part_02(input: &Vec<i32>) -> i32 {
    for (i, a) in input.iter().enumerate() {
        for (j, b) in input.iter().enumerate() {
            for (k, c) in input.iter().enumerate() {
                if i != j && i != k && j != k && a + b + c == 2020 {
                    return a * b * c;
                }
            }
        }
    }

    panic!("failed to find answer");
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

    const EXAMPLE_DATA_1: &'static str = "
    1721
    979
    366
    299
    675
    1456";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 514579)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 241861950);
    }
}
