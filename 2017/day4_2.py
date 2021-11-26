# --- Part Two ---
#
# For added security, yet another system policy has been put in place. Now, a valid passphrase must contain no two
# words that are anagrams of each other - that is, a passphrase is invalid if any word's letters can be rearranged
# to form any other word in the passphrase.
#
# For example:
#
#     abcde fghij is a valid passphrase.
#     abcde xyz ecdab is not valid - the letters from the third word can be rearranged to form the first word.
#     a ab abc abd abf abj is a valid passphrase, because all letters need to be used when forming another word.
#     iiii oiii ooii oooi oooo is valid.
#     oiii ioii iioi iiio is not valid - any of these words can be rearranged to form any other word.
#
# Under this new system policy, how many passphrases are valid?


def is_valid_passphrase(phrase):
    words = [''.join(sorted(word)) for word in phrase.split()]
    return len(set(words)) == len(words)


def main():
    with open('day4_1.input.txt') as f:
        lines = f.readlines()

    print(len([line for line in lines if is_valid_passphrase(line.strip())]))


if __name__ == '__main__':
    main()
