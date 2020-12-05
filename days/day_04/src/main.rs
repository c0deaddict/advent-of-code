use itertools::Itertools;
use lib::run;
use regex::Regex;
use std::collections::HashMap;

#[macro_use]
extern crate lazy_static;

type Passport<'r> = HashMap<&'r str, &'r str>;
type Input<'r> = Vec<Passport<'r>>;

fn parse_input<'r>(input: &'r str) -> Input<'r> {
    input
        .trim()
        .split("\n\n")
        .map(|p| {
            p.trim()
                .split_whitespace()
                .map(|kv| {
                    kv.splitn(2, ":")
                        .collect_tuple()
                        .unwrap()
                })
                .collect()
        })
        .collect()
}

fn has_required_fields(passport: &Passport) -> bool {
    vec!["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
        .iter()
        .map(|f| passport.get(f))
        .all(|v| v.is_some())
}

fn part_01(input: &Input) -> usize {
    input.iter().filter(|p| has_required_fields(p)).count()
}

lazy_static! {
    static ref HAIR_COLOR: Regex = Regex::new(r"^#[0-9a-f]{6}$").unwrap();
    static ref EYE_COLOR: Regex = Regex::new(r"^(amb|blu|brn|gry|grn|hzl|oth)$").unwrap();
    static ref PASSPORT_ID: Regex = Regex::new(r"^[0-9]{9}$").unwrap();
}

fn validate_number(s: &str, min: i32, max: i32) -> bool {
    match s.parse::<i32>() {
        Ok(i) if i >= min && i <= max => true,
        _ => false,
    }
}

fn validate_birth_year(s: &str) -> bool {
    validate_number(s, 1920, 2002)
}

fn validate_issue_year(s: &str) -> bool {
    validate_number(s, 2010, 2020)
}

fn validate_expiration_year(s: &str) -> bool {
    validate_number(s, 2020, 2030)
}

fn validate_height(s: &str) -> bool {
    match s.len() {
        5 => {
            let (height, unit) = s.split_at(3);
            unit == "cm" && validate_number(height, 150, 193)
        }
        4 => {
            let (height, unit) = s.split_at(2);
            unit == "in" && validate_number(height, 59, 76)
        }
        _ => false,
    }
}

fn validate_hair_color(s: &str) -> bool {
    HAIR_COLOR.is_match(s)
}

fn validate_eye_color(s: &str) -> bool {
    EYE_COLOR.is_match(s)
}

fn validate_passport_id(s: &str) -> bool {
    PASSPORT_ID.is_match(s)
}

fn validate_fields(passport: &Passport) -> bool {
    passport.iter().all(|(k, v)| match *k {
        "byr" => validate_birth_year(v),
        "iyr" => validate_issue_year(v),
        "eyr" => validate_expiration_year(v),
        "hgt" => validate_height(v),
        "hcl" => validate_hair_color(v),
        "ecl" => validate_eye_color(v),
        "pid" => validate_passport_id(v),
        _ => true,
    })
}

fn part_02(input: &Input) -> usize {
    input
        .iter()
        .filter(|p| has_required_fields(p))
        .filter(|p| validate_fields(p))
        .count()
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
    ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
    byr:1937 iyr:2017 cid:147 hgt:183cm

    iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
    hcl:#cfa07d byr:1929

    hcl:#ae17e1 iyr:2013
    eyr:2024
    ecl:brn pid:760753108 byr:1931
    hgt:179cm

    hcl:#cfa07d eyr:2025 pid:166559648
    iyr:2011 ecl:brn hgt:59in";

    #[test]
    fn test_parse_input() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(input.len(), 4);
        assert_eq!(input[0].len(), 8);
        assert_eq!(input[0].get("iyr").unwrap(), &"2017");
        assert_eq!(input[3].len(), 6);
        assert_eq!(input[3].get("hgt").unwrap(), &"59in");
    }

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 2);
    }

    #[test]
    fn test_validations() {
        assert_eq!(validate_birth_year("2002"), true);
        assert_eq!(validate_birth_year("2003"), false);

        assert_eq!(validate_height("60in"), true);
        assert_eq!(validate_height("190cm"), true);
        assert_eq!(validate_height("190in"), false);
        assert_eq!(validate_height("190"), false);

        assert_eq!(validate_hair_color("#123abc"), true);
        assert_eq!(validate_hair_color("#123abz"), false);
        assert_eq!(validate_hair_color("123abc"), false);

        assert_eq!(validate_eye_color("brn"), true);
        assert_eq!(validate_eye_color("wat"), false);

        assert_eq!(validate_passport_id("000000001"), true);
        assert_eq!(validate_passport_id("0123456789"), false);
    }

    const INVALID_PASSPORTS: &'static str = "
    eyr:1972 cid:100
    hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

    iyr:2019
    hcl:#602927 eyr:1967 hgt:170cm
    ecl:grn pid:012533040 byr:1946

    hcl:dab227 iyr:2012
    ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

    hgt:59cm ecl:zzz
    eyr:2038 hcl:74454a iyr:2023
    pid:3556412378 byr:2007";

    #[test]
    fn test_invalid_passports() {
        let input = parse_input(INVALID_PASSPORTS);
        assert_eq!(part_02(&input), 0);
    }

    const VALID_PASSPORTS: &'static str = "
    pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
    hcl:#623a2f

    eyr:2029 ecl:blu cid:129 byr:1989
    iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

    hcl:#888785
    hgt:164cm byr:2001 iyr:2015 cid:88
    pid:545766238 ecl:hzl
    eyr:2022

    iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719";

    #[test]
    fn test_valid_passports() {
        let input = parse_input(VALID_PASSPORTS);
        assert_eq!(part_02(&input), 4);
    }
}
