import pytest
import re
from collections import namedtuple

RE_HEADER = """^Begin in state (\w+).
Perform a diagnostic checksum after (\d+) steps\.$"""

RE_STATE = """In state (\w+):
  If the current value is 0:
    - Write the value (\d).
    - Move one slot to the (left|right).
    - Continue with state (\w+).
  If the current value is 1:
    - Write the value (\d).
    - Move one slot to the (left|right).
    - Continue with state (\w+)."""

TuringMachine = namedtuple('TuringMachine', ['begin_state', 'diag_steps', 'states'])
Action = namedtuple('Action', ['write_value', 'move_cursor', 'next_state'])

def parse_input(input):
    blocks = input.strip().split("\n\n")

    # Parse header.
    (begin_state, diag_steps) = re.match(RE_HEADER, blocks[0], re.MULTILINE).groups()

    # Parse states.
    states = {}
    for block in blocks[1:]:
        matches = re.match(RE_STATE, block, re.MULTILINE).groups()
        states[matches[0]] = [
            Action(int(matches[1]), matches[2], matches[3]),
            Action(int(matches[4]), matches[5], matches[6]),
        ]

    return TuringMachine(begin_state, int(diag_steps), states)

def run(machine):
    tape = {}
    cursor = 0
    state = machine.begin_state
    for i in range(machine.diag_steps):
        action = machine.states[state][tape.get(cursor, 0)]
        tape[cursor] = action.write_value
        cursor = cursor - 1 if action.move_cursor == 'left' else cursor + 1
        state = action.next_state
    return tape

def part1(input):
    tape = run(input)
    return sum(tape.values())

def main():
    with open('../input/day_25.txt', 'r') as f:
        input = parse_input(f.read())

    print("part1:", part1(input))

if __name__ == "__main__":
    main()


EXAMPLE_DATA_1 = """
Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
"""

def test_part1():
    assert part1(parse_input(EXAMPLE_DATA_1)) == 3
