use itertools::Itertools;
use lib::run;
use lru::LruCache;
use regex::Regex;
use std::{collections::HashSet, time::Instant};

type Replacements<'a> = Vec<(&'a str, &'a str)>;

#[derive(Debug)]
struct Input<'a> {
    replacements: Replacements<'a>,
    molecule: &'a str,
}

fn parse_input(input: &str) -> Input {
    let (replacements, molecule) = input.trim().splitn(2, "\n\n").collect_tuple().unwrap();

    let replacements = replacements
        .lines()
        .map(|l| l.trim().splitn(2, " => ").collect_tuple().unwrap())
        .sorted_by_key(|(_, to)| to.len())
        .rev()
        .collect();

    let molecule = molecule.trim();

    Input {
        replacements,
        molecule,
    }
}

fn part_01(input: &Input) -> usize {
    let mut result = HashSet::new();
    for (from, to) in &input.replacements {
        for (idx, _) in input.molecule.match_indices(from) {
            let mut new_molecule = input.molecule.to_string();
            new_molecule.replace_range(idx..idx + from.len(), to);
            result.insert(new_molecule);
        }
    }
    result.len()
}

// TODO: find out which letters can come from which patterns.  certain letters
//       like the 'Y' can not be replaced, these can be used as a fixed point to
//       start backward searching.
//
// Y, Rn, Ar, CRn
//
// CRn is not used in the final string, so the rules can be discarded.
// Rn and Ar are always balanced, they are like '(' and ')'
// Y is always between Rn and Ar.
fn find_shortest_path<'a>(
    molecule: &str,
    targets: &[&'a str],
    replacements: &Replacements,
    depth: usize,
    cache: &mut LruCache<String, Option<(&'a str, usize)>>,
) -> Option<(&'a str, usize)> {
    for target in targets {
        if molecule == *target {
            return Some((target, depth));
        }
    }

    if let Some(result) = cache.get(molecule) {
        return *result;
    }

    let options = replacements
        .iter()
        .flat_map(|(from, to)| {
            molecule
                .match_indices(to)
                .map(|(idx, _)| {
                    let mut new_molecule = molecule.to_string();
                    new_molecule.replace_range(idx..idx + to.len(), from);
                    new_molecule
                })
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();

    let count = options.len();
    let mut last_report = Instant::now();
    let mut progress = 0;

    if depth < 10 {
        println!("{} {}", depth, count)
    }

    let result = options
        .iter()
        .filter_map(|m| {
            let result = find_shortest_path(&m, targets, replacements, depth + 1, cache);
            progress += 1;
            if last_report.elapsed().as_secs() >= 2 {
                println!("{} {}/{} {}", depth, progress, count, m);
                last_report = Instant::now();
            }
            result
        })
        .min_by_key(|(_, depth)| *depth);

    cache.put(molecule.to_owned(), result);
    return result;
}

fn split_molecule<'a>(molecule: &'a str) -> Vec<&'a str> {
    let mut tokens = vec![];
    let mut prev = 0;
    let re = Regex::new(r"Rn|Ar").unwrap();
    for m in re.find_iter(molecule) {
        tokens.push(&molecule[prev..m.start()]);
        tokens.push(m.as_str());
        prev = m.end();
    }
    tokens.push(&molecule[prev..]);
    return tokens;
}

fn solve_parens<'a, I>(tokens: &mut I, replacements: &Replacements) -> (String, usize)
where
    I: Iterator<Item = &'a str>,
{
    let mut res = String::new();
    let mut total_depth = 0;

    while let Some(part) = tokens.next() {
        match tokens.next() {
            Some("Rn") => {
                res.push_str(part);
                res.push_str("Rn");
                let (nested, depth) = &solve_parens(tokens, replacements);
                total_depth += depth;
                println!("solve {}", nested);
                let mut cache = LruCache::new(1_000_000);
                let targets = &["Mg", "F", "FYF"];
                let (part, depth) =
                    find_shortest_path(nested, targets, replacements, 0, &mut cache).unwrap();
                total_depth += depth;
                println!("answer: {} => {} (depth {})", nested, part, depth);
                res.push_str(part);
                res.push_str("Ar");
            }
            None | Some("Ar") => {
                res.push_str(part);
                return (res, total_depth);
            }
            t => panic!("unexpected token: {:?}", t),
        }
    }

    panic!("unexpected end");
}

fn part_02(input: &Input) -> usize {
    // Look for strings that can't be replaced by rules.
    let mut fixed_strings = HashSet::new();
    for (_, to) in &input.replacements {
        let mut v = vec![*to];
        for (from, _) in &input.replacements {
            v = v
                .iter()
                .flat_map(|s| s.split(from))
                .filter(|s| !s.is_empty())
                .collect();
        }
        fixed_strings.extend(v);
    }

    for s in fixed_strings {
        println!(
            "Found fixed string: {} (count = {})",
            s,
            input.molecule.matches(s).count()
        );
    }

    let tokens = split_molecule(input.molecule);
    let mut it = tokens.into_iter();
    let simplified = solve_parens(&mut it, &input.replacements);
    println!("{} {} (depth {})", simplified.0.len(), simplified.0, simplified.1);

    let mut cache = LruCache::new(100_000_000);
    let (_, depth) =
        find_shortest_path(&simplified.0, &["e"], &input.replacements, 0, &mut cache).unwrap();
    println!("answer: {}", depth);
    simplified.1 + depth
}

fn main() {
    run(1, include_str!("../../../../input/day_19.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    H => HO
    H => OH
    O => HH

    HOHOHO
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 7)
    }

    const EXAMPLE_DATA_2: &'static str = "
    e => H
    e => O
    H => HO
    H => OH
    O => HH

    HOHOHO
    ";

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_2);
        assert_eq!(part_02(&input), 6)
    }
}
