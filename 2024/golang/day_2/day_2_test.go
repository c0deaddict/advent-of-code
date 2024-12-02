package main

import (
	"strings"
	"testing"
)

const EXAMPLE_1 = `
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
`

func TestPart1(t *testing.T) {
	input := parseInput(strings.TrimSpace(EXAMPLE_1))
	if part1(input) != 2 {
		t.Fail()
	}
}

func TestPart2(t *testing.T) {
	input := parseInput(strings.TrimSpace(EXAMPLE_1))
	if part2(input) != 4 {
		t.Fail()
	}
}
