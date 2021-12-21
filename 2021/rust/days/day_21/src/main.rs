use std::collections::HashMap;

use itertools::Itertools;
use lazy_static::lazy_static;
use lib::run;

#[derive(Debug, Clone, Hash, Eq, PartialEq)]
struct Player {
    pos: u64,
    score: u64,
}

#[derive(Debug, Clone, Hash, Eq, PartialEq)]
struct State {
    players: Vec<Player>,
    turn: usize,
}

type Input = Vec<Player>;

fn parse_input(input: &str) -> Input {
    input
        .trim()
        .lines()
        .map(|l| {
            let (_, pos) = l.splitn(2, ": ").collect_tuple().unwrap();
            let pos = pos.parse().unwrap();
            let score = 0;
            Player { pos, score }
        })
        .collect()
}

fn part_01(input: &Input) -> u64 {
    let mut dice = 0;
    let mut players: Vec<_> = input.iter().cloned().collect();
    let mut turn = 0;
    loop {
        players[turn].pos = 1 + (players[turn].pos + dice * 3 + 5) % 10;
        players[turn].score += players[turn].pos;
        dice += 3;
        if players[turn].score >= 1000 {
            let losing_score = players[(turn + 1) % players.len()].score;
            return dice * losing_score;
        }
        turn = (turn + 1) % players.len();
    }
}

lazy_static! {
    /// Grouped outcomes of three dice rolls.
    static ref DICE_OUTCOMES: Vec<(u64, u64)> = (1..=3)
        .cartesian_product(1..=3)
        .cartesian_product(1..=3)
        .map(|((r1, r2), r3)| r1 + r2 + r3)
        .sorted()
        .group_by(|x| *x)
        .into_iter()
        .map(|(n, group)| (n, group.count() as u64))
        .collect();
}

fn simulate(state: &State, cache: &mut HashMap<State, Vec<u64>>) -> Vec<u64> {
    if let Some(result) = cache.get(state) {
        return result.clone();
    }

    let mut result = vec![0; state.players.len()];
    for (dice, count) in DICE_OUTCOMES.iter() {
        let mut players = state.players.clone();
        let p = &mut players[state.turn];
        p.pos = 1 + (p.pos + dice - 1) % 10;
        p.score += p.pos;
        if p.score >= 21 {
            result[state.turn] += count;
        } else {
            let turn = (state.turn + 1) % state.players.len();
            let next_state = State { players, turn };
            let next_result = simulate(&next_state, cache);
            for (i, next_count) in next_result.iter().enumerate() {
                result[i] += count * next_count;
            }
        }
    }

    cache.insert(state.clone(), result.clone());
    return result;
}

fn part_02(input: &Input) -> u64 {
    let players = input.iter().cloned().collect::<Vec<_>>();
    let turn = 0;
    *simulate(&State { players, turn }, &mut HashMap::new())
        .iter()
        .max()
        .unwrap()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    const EXAMPLE_DATA_1: &'static str = "
    Player 1 starting position: 4
    Player 2 starting position: 8
    ";

    #[test]
    fn example_part_1() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_01(&input), 739785)
    }

    #[test]
    fn example_part_2() {
        let input = parse_input(EXAMPLE_DATA_1);
        assert_eq!(part_02(&input), 444356092776315)
    }
}
