use lib::run;
use std::convert::{TryFrom, TryInto};

#[repr(u8)]
#[derive(Debug, Eq, PartialEq)]
pub enum TypeId {
    Sum = 0,
    Product = 1,
    Minimum = 2,
    Maximum = 3,
    Literal = 4,
    GreaterThan = 5,
    LessThan = 6,
    EqualTo = 7,
}

impl TryFrom<u8> for TypeId {
    type Error = ();

    fn try_from(v: u8) -> Result<Self, Self::Error> {
        match v {
            x if x == TypeId::Sum as u8 => Ok(TypeId::Sum),
            x if x == TypeId::Product as u8 => Ok(TypeId::Product),
            x if x == TypeId::Minimum as u8 => Ok(TypeId::Minimum),
            x if x == TypeId::Maximum as u8 => Ok(TypeId::Maximum),
            x if x == TypeId::Literal as u8 => Ok(TypeId::Literal),
            x if x == TypeId::GreaterThan as u8 => Ok(TypeId::GreaterThan),
            x if x == TypeId::LessThan as u8 => Ok(TypeId::LessThan),
            x if x == TypeId::EqualTo as u8 => Ok(TypeId::EqualTo),
            _ => Err(()),
        }
    }
}

#[derive(Debug, Eq, PartialEq)]
enum Payload {
    Literal(u64),
    Children(Vec<Packet>),
}

#[derive(Debug, Eq, PartialEq)]
struct Packet {
    version: u8,
    type_id: TypeId,
    payload: Payload,
}

type Input = String;

fn parse_input(input: &str) -> Input {
    input.trim().chars().fold(String::new(), |res, ch| {
        res + &format!("{:04b}", u8::from_str_radix(&ch.to_string(), 16).unwrap())
    })
}

fn parse_literal<'a>(bits: &'a str) -> (&'a str, Payload) {
    let mut value = String::new();
    let mut bits = bits;
    loop {
        let stop = &bits[0..=0] == "0";
        value += &bits[1..5];
        bits = &bits[5..];
        if stop {
            break;
        }
    }
    (
        bits,
        Payload::Literal(u64::from_str_radix(&value, 2).unwrap()),
    )
}

fn offset_from(start: &str, offset: &str) -> usize {
    offset.as_ptr() as usize - start.as_ptr() as usize
}

fn parse_operator<'a>(bits: &'a str) -> (&'a str, Payload) {
    let mut children = vec![];
    let (length_type_id, mut bits) = bits.split_at(1);
    match length_type_id {
        "0" => {
            let (total_length, start_bits) = bits.split_at(15);
            let total_length = usize::from_str_radix(total_length, 2).unwrap();
            bits = start_bits;
            while offset_from(start_bits, bits) < total_length {
                let (next_bits, packet) = parse_packet(bits);
                children.push(packet);
                bits = next_bits;
            }
        }
        "1" => {
            let (packet_count, start_bits) = bits.split_at(11);
            let packet_count = usize::from_str_radix(packet_count, 2).unwrap();
            bits = start_bits;
            for _ in 0..packet_count {
                let (next_bits, packet) = parse_packet(bits);
                children.push(packet);
                bits = next_bits;
            }
        }
        _ => panic!("not a bit"),
    };

    (bits, Payload::Children(children))
}

fn parse_packet<'a>(bits: &'a str) -> (&'a str, Packet) {
    let version = u8::from_str_radix(&bits[0..3], 2).unwrap();
    let type_id: TypeId = u8::from_str_radix(&bits[3..6], 2)
        .unwrap()
        .try_into()
        .unwrap();
    let bits = &bits[6..];

    let (bits, payload) = if type_id == TypeId::Literal {
        parse_literal(bits)
    } else {
        parse_operator(bits)
    };

    (
        bits,
        Packet {
            version,
            type_id,
            payload,
        },
    )
}

fn sum_versions(packet: &Packet) -> usize {
    let mut sum = packet.version as usize;
    if let Payload::Children(children) = &packet.payload {
        for child in children {
            sum += sum_versions(&child);
        }
    }
    return sum;
}

fn part_01(input: &Input) -> usize {
    let (_, packet) = parse_packet(input);
    sum_versions(&packet)
}

fn bool_value(b: bool) -> u64 {
    if b {
        1
    } else {
        0
    }
}

fn eval_operator(type_id: &TypeId, children: &Vec<Packet>) -> u64 {
    let mut values = children.iter().map(eval);

    match type_id {
        TypeId::Sum => values.sum(),
        TypeId::Product => values.reduce(|a, b| a * b).unwrap(),
        TypeId::Minimum => values.min().unwrap(),
        TypeId::Maximum => values.max().unwrap(),
        TypeId::GreaterThan => bool_value(values.next().unwrap() > values.next().unwrap()),
        TypeId::LessThan => bool_value(values.next().unwrap() < values.next().unwrap()),
        TypeId::EqualTo => bool_value(values.next().unwrap() == values.next().unwrap()),
        TypeId::Literal => panic!("eval_operator called with Literal"),
    }
}

fn eval(packet: &Packet) -> u64 {
    match &packet.payload {
        Payload::Literal(value) => *value,
        Payload::Children(children) => eval_operator(&packet.type_id, children),
    }
}

fn part_02(input: &Input) -> u64 {
    let (_, packet) = parse_packet(input);
    eval(&packet)
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_literal() {
        assert_eq!(
            parse_literal("101111111000101000"),
            ("000", Payload::Literal(2021))
        );
    }

    #[test]
    fn example_part_1() {
        assert_eq!(part_01(&parse_input("8A004A801A8002F478")), 16);
        assert_eq!(part_01(&parse_input("620080001611562C8802118E34")), 12);
        assert_eq!(part_01(&parse_input("C0015000016115A2E0802F182340")), 23);
        assert_eq!(part_01(&parse_input("A0016C880162017C3686B18A3D4780")), 31);
    }

    #[test]
    fn example_part_2() {
        assert_eq!(part_02(&parse_input("C200B40A82")), 3);
        assert_eq!(part_02(&parse_input("04005AC33890")), 54);
        assert_eq!(part_02(&parse_input("880086C3E88112")), 7);
        assert_eq!(part_02(&parse_input("CE00C43D881120")), 9);
        assert_eq!(part_02(&parse_input("D8005AC2A8F0")), 1);
        assert_eq!(part_02(&parse_input("F600BC2D8F")), 0);
        assert_eq!(part_02(&parse_input("9C005AC2F8F0")), 0);
        assert_eq!(part_02(&parse_input("9C0141080250320F1802104A08")), 1);
    }
}
