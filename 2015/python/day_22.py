import re
from enum import IntEnum
from dataclasses import dataclass, astuple
from copy import deepcopy

from astar import astar


@dataclass
class Player:
    hp: int
    mana: int


@dataclass
class Boss:
    hp: int
    damage: int


class Spell(IntEnum):
    MAGIC_MISSILE = 53
    DRAIN = 73
    SHIELD = 113
    POISON = 173
    RECHARGE = 229

    def cost(self):
        return self.value


@dataclass
class State:
    player: Player
    boss: Boss
    mana_spent: int
    effects: dict[Spell, int]

    def copy(self):
        return deepcopy(self)

    def freeze(self):
        return tuple(
            [astuple(self.player), astuple(self.boss), self.mana_spent]
            + sorted(self.effects.items())
        )

    @staticmethod
    def unfreeze(s) -> "State":
        player, boss, mana_spent, *effects = s
        return State(Player(*player), Boss(*boss), mana_spent, dict(effects))

    def handle_effects(self):
        armor = 0

        # Treat effects.
        for spell in self.effects.keys():
            match spell:
                case Spell.SHIELD:
                    armor = 7
                case Spell.POISON:
                    self.boss.hp -= 3
                case Spell.RECHARGE:
                    self.player.mana += 101

        self.effects = {
            spell: timer - 1 for spell, timer in self.effects.items() if timer > 1
        }

        return armor

    def adjacent(self, hard: bool) -> list[tuple[int, "State"]]:
        if hard:
            self.player.hp -= 1
            if self.player.hp <= 0:
                return []

        self.handle_effects()

        # Boss could die of poison.
        if self.boss.hp <= 0:
            return [(0, self)]

        result = []
        spells = [
            s for s in Spell if self.player.mana >= s.cost() and s not in self.effects
        ]
        for spell in spells:
            # Player turn.
            s = self.copy()
            s.player.mana -= spell.cost()
            s.mana_spent += spell.cost()
            match spell:
                case Spell.MAGIC_MISSILE:
                    s.boss.hp -= 4
                case Spell.DRAIN:
                    s.boss.hp -= 2
                    s.player.hp += 2
                case Spell.SHIELD:
                    s.effects[spell] = 6
                case Spell.POISON:
                    s.effects[spell] = 6
                case Spell.RECHARGE:
                    s.effects[spell] = 5

            # Boss turn, if still alive.
            if s.boss.hp > 0:
                armor = s.handle_effects()
                # Boss could die of poison.
                if s.boss.hp > 0:
                    s.player.hp -= max(s.boss.damage - armor, 1)

            if s.player.hp > 0:
                result.append((spell.cost(), s))

        return result


def parse_input(input) -> Boss:
    return Boss(*map(int, re.findall(r"\d+", input.strip())))


def fight(p: Player, b: Boss, hard: bool):
    start = State(p, b, 0, {}).freeze()

    def adjacent(n):
        return [(c, s.freeze()) for c, s in State.unfreeze(n).adjacent(hard)]

    h = lambda _: 1
    is_target = lambda n: n[1][0] <= 0
    path = astar(start, adjacent, h, is_target)
    return path[-1][2]


def part1(input):
    return fight(Player(50, 500), input, False)


def part2(input):
    return fight(Player(50, 500), input, True)


def main():
    with open("../input/day_22.txt", "r") as f:
        input = parse_input(f.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()


def test_part1():
    assert fight(Player(10, 250), Boss(13, 8)) == 226
    assert fight(Player(10, 250), Boss(14, 8)) == 641
