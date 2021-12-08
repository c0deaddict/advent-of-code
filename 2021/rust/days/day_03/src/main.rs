use lib::run;

type Input = Vec<Vec<char>>;

fn parse_input(input: &str) -> Input {
    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| l.chars().collect())
        .collect()
}

fn count_bits(input: &Input, pos: usize) -> (usize, usize) {
    input.iter().fold((0, 0), |(zero, one), s| {
        if s[pos] == '0' {
            (zero + 1, one)
        } else {
            (zero, one + 1)
        }
    })
}

fn count_all_bits(input: &Input) -> Vec<(usize, usize)> {
    (0..input[0].len()).map(|i| count_bits(input, i)).collect()
}

fn most_common(count: &(usize, usize)) -> char {
    if count.1 >= count.0 {
        '1'
    } else {
        '0'
    }
}

fn least_common(count: &(usize, usize)) -> char {
    if count.0 <= count.1 {
        '0'
    } else {
        '1'
    }
}

fn part_01(input: &Input) -> u32 {
    let counts = count_all_bits(input);
    let gamma_bits: String = counts.iter().map(most_common).collect();
    let epsilon_bits: String = counts.iter().map(least_common).collect();
    let gamma_rate = u32::from_str_radix(&gamma_bits, 2).unwrap();
    let epsilon_rate = u32::from_str_radix(&epsilon_bits, 2).unwrap();
    gamma_rate * epsilon_rate
}

fn find_bit_criteria(input: &Input, select: fn(&(usize, usize)) -> char) -> String {
    let bits = input[0].len();
    let mut list = input.clone();
    for i in 0..bits {
        let b = select(&count_bits(&list, i));
        list.retain(|s| s[i] == b);
        if list.len() == 1 {
            return list[0].iter().collect();
        }
    }
    panic!("multiple bits are left");
}

fn part_02(input: &Input) -> u32 {
    let oxygen_bits = find_bit_criteria(input, most_common);
    let co2_bits = find_bit_criteria(input, least_common);
    let oxygen_rating = u32::from_str_radix(&oxygen_bits, 2).unwrap();
    let co2_rating = u32::from_str_radix(&co2_bits, 2).unwrap();
    oxygen_rating * co2_rating
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    00100
    11110
    10110
    10111
    10101
    01111
    00111
    11100
    10000
    11001
    00010
    01010
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 198);
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 230);
    }
}
