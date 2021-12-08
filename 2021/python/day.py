def main():
    with open("input.txt", "r") as file:
        input = parse_input(file.read())

    print("part1:", part1(input))
    print("part2:", part2(input))


if __name__ == "__main__":
    main()
