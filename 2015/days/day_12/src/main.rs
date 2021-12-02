use json::JsonValue;
use lib::run;
use std::convert::TryInto;

type Input = JsonValue;

fn parse_input(input: &str) -> Input {
    json::parse(input).unwrap()
}

fn sum_json(value: &JsonValue) -> i64 {
    match value {
        JsonValue::Number(_) => value.as_i64().unwrap(),
        JsonValue::Array(arr) => arr.iter().map(sum_json).sum(),
        JsonValue::Object(obj) => obj.iter().map(|(_, val)| sum_json(val)).sum(),
        _ => 0,
    }
}

fn part_01(input: &Input) -> i64 {
    sum_json(input)
}

fn sum_json_part2(value: &JsonValue) -> i64 {
    match value {
        JsonValue::Number(_) => value.as_i64().unwrap(),
        JsonValue::Array(arr) => arr.iter().map(sum_json_part2).sum(),
        JsonValue::Object(obj) => {
            if obj.iter().any(|(_, val)| val.is_string() && val == "red") {
                0
            } else {
                obj.iter().map(|(_, val)| sum_json_part2(val)).sum()
            }
        }
        _ => 0,
    }
}

fn part_02(input: &Input) -> i64 {
    sum_json_part2(input)
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example_part_1() {
        let input = parse_input(r#"{"a":{"b":4},"c":-1}"#);
        assert_eq!(part_01(&input), 3);
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(r#"{"d":"red","e":[1,2,3,4],"f":5}"#);
        assert_eq!(part_02(&input), 0)
    }
}
