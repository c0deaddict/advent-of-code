use lib::run;
use regex::Regex;

type Props = Vec<i64>;
type Input<'a> = Vec<Props>;

fn parse_input(input: &str) -> Input {
    let re = Regex::new(r"-?\d+").unwrap();

    input
        .lines()
        .map(|l| l.trim())
        .filter(|l| !l.is_empty())
        .map(|l| {
            re.find_iter(l)
                .filter_map(|d| d.as_str().parse().ok())
                .collect()
        })
        .collect()
}

fn add_ingredient(total: &Props, ingredient: &Props, count: usize) -> Props {
    let mut res = total.clone();
    for i in 0..5 {
        res[i] += ingredient[i] * (count as i64);
    }
    res
}

// Idea: scan per property (per column; summing over all ingredients). if the
// sum <= 0 then we can discard the ingredient ratio earlier.
fn maximize_score(
    ingredients: &[Props],
    count: usize,
    total: &Props,
    total_calories: Option<i64>,
) -> i64 {
    if ingredients.is_empty() {
        panic!("maximize_score called without ingredients");
    }

    let current = ingredients[0].clone();
    let ingredients = &ingredients[1..];

    (1..(101 - count - ingredients.len()))
        .map(|i| {
            let total = add_ingredient(total, &current, i);
            if ingredients.is_empty() {
                if let Some(total_calories) = total_calories {
                    if total[4] != total_calories {
                        return 0;
                    }
                }

                total[0..4]
                    .iter()
                    .map(|x| if *x < 0 { 0 } else { *x })
                    .reduce(|a, b| a * b)
                    .unwrap()
            } else {
                maximize_score(ingredients, count + i, &total, total_calories)
            }
        })
        .max()
        .unwrap()
}

fn part_01(input: &Input) -> i64 {
    maximize_score(input, 0, &vec![0; 5], None)
}

fn part_02(input: &Input) -> i64 {
    maximize_score(input, 0, &vec![0; 5], Some(500))
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
    Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 62842880)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 57600000)
    }
}
