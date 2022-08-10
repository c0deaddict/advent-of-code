import pytest
import re
from dataclasses import dataclass
from typing import List
from functools import cmp_to_key
from operator import attrgetter
import copy
import itertools


@dataclass
class Group:
    system: int
    idx: int
    units: int
    hp: int
    attack_type: str
    attack_damage: int
    initiative: int
    immune: List[str]
    weak: List[str]

    def effective_power(self):
        return self.units * self.attack_damage

    def compute_damage_from(self, other: "Group") -> int:
        damage = other.effective_power()
        if other.attack_type in self.weak:
            damage = damage * 2
        elif other.attack_type in self.immune:
            damage = 0
        return damage

    def take_damage_from(self, other: "Group") -> int:
        amount = self.compute_damage_from(other)
        killed_units = min(self.units, amount // self.hp)
        self.units -= killed_units
        return killed_units

    def name(self) -> str:
        system_str = "Infection" if self.system == 1 else "Immune system"
        return f"{system_str} group {self.idx+1}"


def parse_group(system, idx, line):
    units, hp, attack_damage, initiative = map(int, re.findall("(\d+)", line))
    attack_type = re.findall(r"\d+ (\w+) damage", line)[0]
    group = Group(
        system, idx, units, hp, attack_type, attack_damage, initiative, [], []
    )
    weak_immune = re.findall(r"\(([^\)]+)\)", line)
    if weak_immune:
        for part in weak_immune[0].split("; "):
            what, _, attacks = part.split(" ", 2)
            attacks = attacks.strip().split(", ")
            if what == "weak":
                group.weak = attacks
            else:
                group.immune = attacks
    return group


def parse_input(input):
    parts = input.strip().split("\n\n")
    return [
        [
            parse_group(system, idx, line)
            for idx, line in enumerate(groups.splitlines()[1:])
        ]
        for system, groups in enumerate(parts)
    ]


def sort_for_target_selection(groups):
    def compare(a, b):
        diff = a.effective_power() - b.effective_power()
        if diff != 0:
            return diff
        return a.initiative - b.initiative

    return sorted(groups, key=cmp_to_key(compare), reverse=True)


def select_target(attacker, defenders):
    def compare(a, b):
        diff = a.compute_damage_from(attacker) - b.compute_damage_from(attacker)
        if diff != 0:
            return diff
        diff = a.effective_power() - b.effective_power()
        if diff != 0:
            return diff
        return a.initiative - b.initiative

    target = max(defenders, key=cmp_to_key(compare))
    if target.compute_damage_from(attacker) == 0:
        return None
    else:
        return target


def debug_print(*args):
    # print(*args)
    pass


def target_selection(attackers, defenders):
    selection = [None] * len(attackers)
    defenders = [d for d in defenders if d.units > 0]
    for attacker in sort_for_target_selection(attackers):
        if len(defenders) == 0:
            break
        target = select_target(attacker, defenders)
        if target:
            selection[attacker.idx] = (target.system, target.idx)
            defenders = [d for d in defenders if d != target]
            debug_print(
                f"{attacker.name()} would deal {target.name()} {target.compute_damage_from(attacker)} damage"
            )
        else:
            debug_print(f"{attacker.name()} could not find a defending group to attack")
    return selection


def round(input):
    total_units_killed = 0
    a, b = input
    selection = [target_selection(a, b), target_selection(b, a)]
    debug_print()
    for attacker in sorted(a + b, key=attrgetter("initiative"), reverse=True):
        target = selection[attacker.system][attacker.idx]
        if target:
            system, group = target
            units_killed = input[system][group].take_damage_from(attacker)
            debug_print(
                f"{attacker.name()} attacks {input[system][group].name()}, killing {units_killed} units"
            )
            total_units_killed += units_killed
    return total_units_killed


def sum_units(system):
    return sum(map(attrgetter("units"), system))


def game_over(input):
    return any((sum_units(s) == 0 for s in input))


def run(input):
    input = copy.deepcopy(input)
    while not game_over(input):
        debug_print()
        if round(input) == 0:
            return None
        debug_print()
        for system in input:
            for group in system:
                debug_print(f"{group.name()} contains {group.units} units")
    debug_print()
    return [sum_units(s) for s in input]


def part1(input):
    return max(run(input))


def boost(input, amount):
    result = copy.deepcopy(input)
    for group in result[0]:
        group.attack_damage += amount
    return result


def part2(input):
    for amount in itertools.count(start=1):
        result = run(boost(input, amount))
        if result and result[0] != 0:
            return result[0]


def main():
    with open("../input/day_24.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


EXAMPLE_DATA_1 = """
Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4
"""


def test_part1():
    assert part1(parse_input(EXAMPLE_DATA_1)) == 5216


def test_part2():
    assert part2(parse_input(EXAMPLE_DATA_1)) == 51
