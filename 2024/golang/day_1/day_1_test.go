package main

import (
	"strings"
	"testing"
)

const EXAMPLE_1 = `
3   4
4   3
2   5
1   3
3   9
3   3
`

func TestPart1(t *testing.T) {
	if part1(parseInput(strings.TrimSpace(EXAMPLE_1))) != 11 {
		t.Fail()
	}
}

func TestPart2(t *testing.T) {
	if part2(parseInput(strings.TrimSpace(EXAMPLE_1))) != 31 {
		t.Fail()
	}
}
