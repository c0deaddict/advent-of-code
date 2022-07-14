use itertools::Itertools;
use lazy_static::lazy_static;
use lib::run;
use regex::Regex;
use std::cmp;
use std::collections::HashMap;

use Spell::*;

#[derive(Debug, Clone)]
struct Player {
    hp: i32,
    mana: i32,
}

#[derive(Debug, Clone)]
struct Boss {
    hp: i32,
    damage: i32,
}

type Input = Boss;

fn parse_input(input: &str) -> Input {
    let re = Regex::new(r"^Hit Points: (\d+)\nDamage: (\d+)$").unwrap();

    let (hp, damage) = re
        .captures(input.trim())
        .unwrap()
        .iter()
        .skip(1)
        .map(|c| c.unwrap().as_str().parse().unwrap())
        .collect_tuple()
        .unwrap();

    Boss { hp, damage }
}

#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy)]
enum Spell {
    MagicMissile,
    Drain,
    Shield,
    Poison,
    Recharge,
}

impl Spell {
    fn cost(&self) -> i32 {
        match self {
            MagicMissile => 53,
            Drain => 73,
            Shield => 113,
            Poison => 173,
            Recharge => 229,
        }
    }

    fn is_effect(&self) -> bool {
        self.effect_len().is_some()
    }

    fn effect_len(&self) -> Option<usize> {
        match self {
            MagicMissile | Drain => None,
            Poison | Shield => Some(6),
            Recharge => Some(5),
        }
    }
}

fn fight(me: &Player, boss: &Boss, spells: &Vec<Spell>) -> bool {
    let mut spells = spells.iter().cloned();
    let mut me = me.clone();
    let mut boss = boss.clone();
    let mut effects = HashMap::new();
    let mut my_turn = true;

    loop {
        let mut armor = 0;

        // Treat effects.
        for (spell, timer) in &mut effects {
            match spell {
                Shield => armor = 7,
                Poison => boss.hp -= 3,
                Recharge => me.mana += 101,
                _ => panic!("not a valid effect: {:?}", spell),
            }
            *timer -= 1;
        }

        // Effects wear off when timer == 0.
        effects.retain(|_, timer| *timer > 0);

        // Boss could die of Poison.
        if boss.hp <= 0 {
            return true;
        }

        if my_turn {
            let spell = match spells.next() {
                Some(s) => s,
                None => return false, // Not enough spells.
            };

            me.mana -= spell.cost();
            if me.mana < 0 {
                return false; // Out of mana = Lose.
            }

            if spell.is_effect() && effects.contains_key(&spell) {
                return false; // Spell is not valid, effect is active.
            }

            match spell {
                MagicMissile => boss.hp -= 4,
                Drain => {
                    boss.hp -= 2;
                    me.hp += 2;
                }
                _ => {
                    effects.insert(spell, spell.effect_len().unwrap());
                }
            }

            if boss.hp <= 0 {
                return true;
            }
        } else {
            me.hp -= cmp::max(boss.damage - armor, 1);
            if me.hp <= 0 {
                return false;
            }
        }

        my_turn = !my_turn;
    }
}

lazy_static! {
    static ref SPELLS: Vec<Spell> = vec![MagicMissile, Drain, Shield, Poison, Recharge];
}

struct SpellPermutations {
    state: Vec<usize>,
    done: bool,
}

impl SpellPermutations {
    fn new(n: usize) -> Self {
        Self {
            state: vec![0; n],
            done: false,
        }
    }

    fn next_state(&mut self) {
        self.state[0] += 1;
        let mut carry = false;
        for i in 0..self.state.len() {
            carry = self.state[i] >= SPELLS.len();
            if carry {
                self.state[i] = 0;
                if i + 1 < self.state.len() {
                    self.state[i + 1] += 1;
                }
            } else {
                break;
            }
        }

        if carry {
            self.done = true;
        }
    }

    /// Make sure effects are spaced apart far enough.
    fn is_valid_state(&self) -> bool {
        let mut last = vec![None; SPELLS.len()];
        for (i, s) in self.state.iter().enumerate() {
            if let Some(effect_len) = SPELLS[*s].effect_len() {
                if let Some(j) = last[*s] {
                    if i - j < effect_len {
                        return false;
                    }
                }
                last[*s] = Some(i);
            }
        }
        return true;
    }
}

impl Iterator for SpellPermutations {
    type Item = Vec<Spell>;

    fn next(&mut self) -> Option<Self::Item> {
        while !self.done && !self.is_valid_state() {
            self.next_state();
        }

        if self.done {
            return None;
        }

        let result = self.state.iter().map(|i| SPELLS[*i]).collect();
        self.next_state();
        return Some(result);
    }
}

fn part_01(input: &Input) -> i32 {
    let me = Player { hp: 50, mana: 500 };
    let boss = input;

    (14..15)
        .flat_map(|n| SpellPermutations::new(n))
        .filter_map(|spells| {
            if fight(&me, &boss, &spells) {
                Some(spells.iter().map(Spell::cost).sum())
            } else {
                None
            }
        })
        .min()
        .unwrap()
}

fn part_02(input: &Input) -> i32 {
    panic!("failed to find answer");
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example_1_part_1() {
        let me = Player { hp: 10, mana: 250 };
        let boss = Boss { hp: 13, damage: 8 };
        let spells = vec![Poison, MagicMissile];
        assert_eq!(fight(&me, &boss, &spells), true);
    }

    #[test]
    fn example_2_part_1() {
        let me = Player { hp: 10, mana: 250 };
        let boss = Boss { hp: 14, damage: 8 };
        let spells = vec![Recharge, Shield, Drain, Poison, MagicMissile];
        assert_eq!(fight(&me, &boss, &spells), true);
    }
}
