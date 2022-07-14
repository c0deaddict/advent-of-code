use itertools::Itertools;
use lib::run;
use regex::Regex;
use std::cmp;

#[derive(Debug)]
struct Player {
    hp: i32,
    damage: i32,
    armor: i32,
}

#[derive(Debug, Clone)]
struct Item<'a> {
    name: &'a str,
    cost: i32,
    damage: i32,
    armor: i32,
}

#[derive(Default, Debug)]
struct Inventory<'a> {
    weapons: Vec<Item<'a>>,
    armor: Vec<Item<'a>>,
    rings: Vec<Item<'a>>,
}

type Input = Player;

fn parse_input(input: &str) -> Input {
    let re = Regex::new(r"^Hit Points: (\d+)\nDamage: (\d+)\nArmor: (\d+)$").unwrap();

    let (hp, damage, armor) = re
        .captures(input.trim())
        .unwrap()
        .iter()
        .skip(1)
        .map(|c| c.unwrap().as_str().parse().unwrap())
        .collect_tuple()
        .unwrap();

    Player { hp, damage, armor }
}

fn parse_inventory<'a>(input: &'a str) -> Inventory<'a> {
    let mut inventory = Inventory::default();
    let whitespace_re = Regex::new(r"\s{2,}").unwrap();

    for chunk in input.trim().split("\n\n") {
        let mut it = chunk.lines();
        let header = it.next().unwrap();
        let group = match header.splitn(2, ": ").next().unwrap() {
            "Weapons" => &mut inventory.weapons,
            "Armor" => &mut inventory.armor,
            "Rings" => &mut inventory.rings,
            group => panic!("undefined inventory group {}", group),
        };

        for line in it {
            let mut cols = whitespace_re.split(line).map(|s| s.trim());
            let name = cols.next().unwrap();
            let (cost, damage, armor) = cols.map(|s| s.parse().unwrap()).collect_tuple().unwrap();
            group.push(Item {
                name,
                cost,
                damage,
                armor,
            })
        }
    }

    inventory
}

fn read_inventory() -> Inventory<'static> {
    parse_inventory(include_str!("inventory.txt"))
}

fn fight(me: &Player, boss: &Player) -> bool {
    let mut my_hp = me.hp;
    let mut boss_hp = boss.hp;
    let mut my_turn = true;
    while my_hp > 0 && boss_hp > 0 {
        if my_turn {
            boss_hp -= cmp::max(me.damage - boss.armor, 0)
        } else {
            my_hp -= cmp::max(boss.damage - me.armor, 0)
        }

        my_turn = !my_turn;
    }

    my_hp > 0
}

fn player_cost_permutations<'a>(
    inventory: &'a Inventory<'a>,
) -> impl Iterator<Item = (Player, i32)> + 'a {
    let weapons = inventory.weapons.iter();

    let mut armor = vec![&Item {
        name: "No armor",
        cost: 0,
        damage: 0,
        armor: 0,
    }];
    armor.extend(inventory.armor.iter());

    let mut rings = vec![vec![]]; // No rings
    rings.extend(inventory.rings.iter().combinations(1));
    rings.extend(inventory.rings.iter().combinations(2));

    weapons
        .cartesian_product(armor)
        .cartesian_product(rings)
        .map(|((weapon, armor), rings)| {
            let mut p = Player {
                hp: 100,
                damage: weapon.damage,
                armor: armor.armor,
            };
            let mut cost = weapon.cost + armor.cost;
            for r in rings {
                p.damage += r.damage;
                p.armor += r.armor;
                cost += r.cost;
            }
            (p, cost)
        })
}

fn part_01(input: &Input) -> i32 {
    let boss = input;
    player_cost_permutations(&read_inventory())
        .filter(|(me, _)| fight(&me, &boss))
        .map(|(_, cost)| cost)
        .min()
        .unwrap()
}

fn part_02(input: &Input) -> i32 {
    let boss = input;
    player_cost_permutations(&read_inventory())
        .filter(|(me, _)| !fight(&me, &boss))
        .map(|(_, cost)| cost)
        .max()
        .unwrap()
}

fn main() {
    run(1, include_str!("input.txt"), parse_input, part_01, part_02)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example_part_1() {
        let me = Player {
            hp: 8,
            damage: 5,
            armor: 5,
        };
        let boss = Player {
            hp: 12,
            damage: 7,
            armor: 2,
        };
        assert_eq!(fight(&me, &boss), true);
    }
}
