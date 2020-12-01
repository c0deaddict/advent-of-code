use clap::{App, Arg};
use std::fmt::Debug;
use std::time::Instant;

type ParseInput<I> = dyn Fn(&str) -> I;
type Part<I, T> = dyn Fn(&I) -> T;

pub fn run<I, T1: Debug, T2: Debug>(
    num: u32,
    input: &str,
    parse_input: &ParseInput<I>,
    part_01: &Part<I, T1>,
    part_02: &Part<I, T2>,
) {
    let matches = App::new(format!("AOC 2020 day {}", num))
        .author("Jos van Bakel")
        .about("Advent of Code 2020 solutions")
        .arg(Arg::with_name("part").short("p").takes_value(true))
        .arg(Arg::with_name("benchmark").short("b"))
        .get_matches();

    let input = parse_input(input);

    match matches.value_of("part") {
        Some("1") => run_part("1", || part_01(&input)),
        Some("2") => run_part("2", || part_02(&input)),
        _ => {
            run_part("1", || part_01(&input));
            run_part("2", || part_02(&input));
        }
    }
}

fn run_part<T: Debug, F: FnOnce() -> T>(part: &str, f: F) {
    let now = Instant::now();
    let result = f();
    println!("Part {}: {:?} ({:.2?})", part, result, now.elapsed());
}
