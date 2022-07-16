# --- Part Two ---

# Out of curiosity, the debugger would also like to know the size of the loop: starting from a state that has already
# been seen, how many block redistribution cycles must be performed before that same state is seen again?
#
# In the example above, 2 4 1 2 is seen again after four cycles, and so the answer in that example would be 4.
#
# How many cycles are in the infinite loop that arises from the configuration in your puzzle input?


def cycle(state):
    blocks = max(state)
    index = state.index(blocks)

    new_state = state[:]
    new_state[index] = 0
    for i in range(blocks):
        new_state[(index + i + 1) % len(new_state)] += 1

    return new_state


def serialize_state(state):
    return ",".join(map(str, state))


def solve(input):
    state = input
    states_seen = {serialize_state(state)}

    while True:
        state = cycle(state)
        if serialize_state(state) in states_seen:
            break
        else:
            states_seen.add(serialize_state(state))

    return state, len(states_seen)


def main():
    input = [4, 1, 15, 12, 0, 9, 9, 5, 5, 8, 7, 3, 14, 5, 12, 3]
    state, _ = solve(input)
    _, loop_len = solve(state)
    print(loop_len)


if __name__ == "__main__":
    main()
