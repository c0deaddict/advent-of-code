# --- Day 9: Stream Processing ---
#
# A large stream blocks your path. According to the locals, it's not safe to cross the stream at the moment because
# it's full of garbage. You look down at the stream; rather than water, you discover that it's a stream of characters.
#
# You sit for a while and record part of the stream (your puzzle input). The characters represent groups - sequences
# that begin with { and end with }. Within a group, there are zero or more other things, separated by commas: either
# another group or garbage. Since groups can contain other groups, a } only closes the most-recently-opened unclosed
# group - that is, they are nestable. Your puzzle input represents a single, large group which itself contains many
# smaller ones.
#
# Sometimes, instead of a group, you will find garbage. Garbage begins with < and ends with >. Between those angle
# brackets, almost any character can appear, including { and }. Within garbage, < has no special meaning.
#
# In a futile attempt to clean up the garbage, some program has canceled some of the characters within it using !:
# inside garbage, any character that comes after ! should be ignored, including <, >, and even another !.
#
# You don't see any characters that deviate from these rules. Outside garbage, you only find well-formed groups, and
# garbage always terminates according to the rules above.
#
# Here are some self-contained pieces of garbage:
#
# <>, empty garbage.
# <random characters>, garbage containing random characters.
# <<<<>, because the extra < are ignored.
# <{!>}>, because the first > is canceled.
# <!!>, because the second ! is canceled, allowing the > to terminate the garbage.
# <!!!>>, because the second ! and the first > are canceled.
# <{o"i!a,<{i<a>, which ends at the first >.
#
# Here are some examples of whole streams and the number of groups they contain:
#
# {}, 1 group.
# {{{}}}, 3 groups.
# {{},{}}, also 3 groups.
# {{{},{},{{}}}}, 6 groups.
# {<{},{},{{}}>}, 1 group (which itself contains garbage).
# {<a>,<a>,<a>,<a>}, 1 group.
# {{<a>},{<a>},{<a>},{<a>}}, 5 groups.
# {{<!>},{<!>},{<!>},{<a>}}, 2 groups (since all but the last > are canceled).
#
# Your goal is to find the total score for all groups in your input. Each group is assigned a score which is one more
# than the score of the group that immediately contains it. (The outermost group gets a score of 1.)
#
# {}, score of 1.
# {{{}}}, score of 1 + 2 + 3 = 6.
# {{},{}}, score of 1 + 2 + 2 = 5.
# {{{},{},{{}}}}, score of 1 + 2 + 3 + 3 + 3 + 4 = 16.
# {<a>,<a>,<a>,<a>}, score of 1.
# {{<ab>},{<ab>},{<ab>},{<ab>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
# {{<!!>},{<!!>},{<!!>},{<!!>}}, score of 1 + 2 + 2 + 2 + 2 = 9.
# {{<a!>},{<a!>},{<a!>},{<ab>}}, score of 1 + 2 = 3.
# What is the total score for all groups in your input?
#


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
    return res


def parse_garbage(stream):
    res = '<'
    while not stream.accept('>'):
        if stream.peek() is None:
            raise ValueError("expected '>'")
        elif stream.accept('!'):
            res += '!' + stream.next()
        else:
            res += stream.next()

    return res + '>'


def parse(input):
    stream = Stream(input)
    result = parse_group(stream)
    if not stream.peek() is None:
        raise ValueError('not at end of stream')
    return result


def score(group, depth=1):
    return depth + sum([score(sub, depth+1) for sub in group if type(sub) is list])


def main():
    with open('../input/day9_1.input.txt') as f:
        group = parse(f.read())
        print(score(group))


if __name__ == '__main__':
    main()
