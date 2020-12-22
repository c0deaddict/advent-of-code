use itertools::Itertools;
use lib::run;
use std::collections::{HashSet, VecDeque};

type Deck = VecDeque<usize>;
type Input = (Deck, Deck);

fn parse_deck(input: &str) -> Deck {
    let mut it = input.trim().lines();
    let _player = it.next();
    it.map(|line| line.trim().parse().unwrap()).collect()
}

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .splitn(2, "\n\n")
        .map(parse_deck)
        .collect_tuple()
        .unwrap()
}

fn play<'a>(p1: &'a mut Deck, p2: &'a mut Deck) -> &'a Deck {
    while !p1.is_empty() && !p2.is_empty() {
        let c1 = p1.pop_front().unwrap();
        let c2 = p2.pop_front().unwrap();

        if c1 > c2 {
            p1.push_back(c1);
            p1.push_back(c2);
        } else {
            p2.push_back(c2);
            p2.push_back(c1);
        }
    }

    if p1.is_empty() {
        p2
    } else {
        p1
    }
}

fn score(d: &Deck) -> usize {
    d.iter()
        .rev()
        .enumerate()
        .map(|(i, card)| card * (i + 1))
        .sum()
}

fn part1(input: &Input) -> usize {
    let mut input = input.clone();
    score(play(&mut input.0, &mut input.1))
}

fn play_recursive<'a>(p1: &'a mut Deck, p2: &'a mut Deck, depth: usize) -> (bool, &'a Deck) {
    let mut prev_rounds = HashSet::new();

    println!("");
    println!("=== Game {} ===", depth + 1);
    println!("");

    let mut round = 0;
    while !p1.is_empty() && !p2.is_empty() {
        println!("-- Round {} (Game {}) --", round + 1, depth + 1);
        println!("Player 1's deck: {:?}", p1);
        println!("Player 2's deck: {:?}", p2);

        if !prev_rounds.insert((p1.clone(), p2.clone())) {
            // Game ends instantly, p1 wins.
            println!("Repetition: p1 wins");
            return (true, p1);
        }

        let c1 = p1.pop_front().unwrap();
        let c2 = p2.pop_front().unwrap();
        println!("Player 1 plays: {}", c1);
        println!("Player 2 plays: {}", c2);

        let p1_won_round = if p1.len() >= c1 && p2.len() >= c2 {
            // Recursive game determines winner of the round.
            println!("Playing a sub-game to determine the winner...");
            let mut p1 = p1.iter().cloned().take(c1).collect();
            let mut p2 = p2.iter().cloned().take(c2).collect();
            play_recursive(&mut p1, &mut p2, depth + 1).0
        } else {
            // Normal rules.
            c1 > c2
        };

        if p1_won_round {
            println!("Player 1 wins round {} of game {}!", round + 1, depth + 1);
            p1.push_back(c1);
            p1.push_back(c2);
        } else {
            println!("Player 2 wins round {} of game {}!", round + 1, depth + 1);
            p2.push_back(c2);
            p2.push_back(c1);
        };

        println!("");

        round += 1;
    }

    if !p1.is_empty() {
        (true, p1)
    } else {
        (false, p2)
    }
}

fn part2(input: &Input) -> usize {
    let mut players = input.clone();
    let deck = play_recursive(&mut players.0, &mut players.1, 0).1;
    score(deck)
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part1, part2)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    Player 1:
    9
    2
    6
    3
    1

    Player 2:
    5
    8
    4
    7
    10";

    #[test]
    fn example_1_part1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part1(&input), 306);
    }

    #[test]
    fn example_1_part2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part2(&input), 291);
    }
}
