use lib::run;

type Input = usize;

fn parse_input(input: &str) -> Input {
    input.trim().parse().unwrap()
}

fn part_01(input: &Input) -> usize {
    (1..)
        .find(|i| {
            let mut sum = (i + 1) * 10;
            let limit = (*i as f64).sqrt() as usize;
            // Divisors come in pairs.
            for j in 2..=limit {
                if i % j == 0 {
                    sum += 10 * j;
                    if i / j != j {
                        sum += 10 * (i / j);
                    }
                }
            }
            sum >= *input
        })
        .unwrap()
}

#[inline(always)]
fn elf_visits_house(elf: usize, house: usize) -> bool {
    house / elf <= 50
}

fn part_02(input: &Input) -> usize {
    (51..)
        .find(|i| {
            let mut sum = i * 11;
            let limit = (*i as f64).sqrt() as usize;
            // Divisors come in pairs.
            for j in 2..=limit {
                if i % j == 0 {
                    if elf_visits_house(j, *i) {
                        sum += 11 * j;
                    }
                    let d = i / j;
                    if d != j && elf_visits_house(d, *i) {
                        sum += 11 * d;
                    }
                }
            }
            sum >= *input
        })
        .unwrap()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}
