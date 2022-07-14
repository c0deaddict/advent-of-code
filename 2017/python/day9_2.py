# --- Part Two ---
#
# Now, you're ready to remove the garbage.
#
# To prove you've removed it, you need to count all of the characters within the garbage. The leading and trailing <
# and > don't count, nor do any canceled characters or the ! doing the canceling.
#
#     <>, 0 characters.
#     <random characters>, 17 characters.
#     <<<<>, 3 characters.
#     <{!>}>, 2 characters.
#     <!!>, 0 characters.
#     <!!!>>, 0 characters.
#     <{o"i!a,<{i<a>, 10 characters.
#
# How many non-canceled characters are within the garbage in your puzzle input?


class Stream(object):
    def __init__(self, input):
        self.input = input
        self.pos = 0

    def peek(self):
        try:
            return self.input[self.pos]
        except IndexError:
            return None

    def next(self):
        res = self.peek()
        if res is not None:
            self.pos += 1
        return res

    def accept(self, ch):
        if self.peek() == ch:
            self.next()
            return True
        return False


def parse_group(stream):
    if not stream.accept('{'):
        raise ValueError("group must start with '{'")

    res = []
    while not stream.accept('}'):
        if stream.peek() is None:
            raise ValueError('unterminated group')
        res.append(parse_element(stream))
        if not stream.accept(','):
            if not stream.accept('}'):
                raise ValueError("expected end of group '}'")
            break

    return res


def parse_element(stream):
    if stream.peek() == '{':
        return parse_group(stream)
    elif stream.accept('<'):
        return parse_garbage(stream)
    else:
        return parse_string(stream)


def parse_string(stream):
    res = ''
    while stream.peek() not in [None, ',', '{', '}']:
        res += stream.next()
    return 'string', res


def parse_garbage(stream):
    res = ''
    while not stream.accept('>'):
        if stream.peek() is None:
            raise ValueError("expected '>'")
        elif stream.accept('!'):
            stream.next()
        else:
            res += stream.next()

    return 'garbage', res


def parse(input):
    stream = Stream(input)
    result = parse_group(stream)
    if not stream.peek() is None:
        raise ValueError('not at end of stream')
    return result


def score(group, depth=1):
    return depth + sum([score(sub, depth+1) for sub in group if type(sub) is list])


def count_garbage(node):
    if type(node) is list:
        return sum(map(count_garbage, node))
    elif node[0] == 'garbage':
        return len(node[1])
    else:
        return 0


def main():
    with open('../input/day9_1.input.txt') as f:
        group = parse(f.read())
        print(count_garbage(group))


if __name__ == '__main__':
    main()
