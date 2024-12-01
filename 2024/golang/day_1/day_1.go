package main

import (
	"bufio"
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

type Input = [2][]int

func parseInput(input string) Input {
	var lists [2][]int
	sc := bufio.NewScanner(strings.NewReader(input))
	for sc.Scan() {
		fields := strings.Fields(sc.Text())
		for i := 0; i < len(lists); i++ {
			v, err := strconv.Atoi(fields[i])
			if err != nil {
				panic(err)
			}
			lists[i] = append(lists[i], v)
		}
	}
	return lists
}

func part1(input Input) int {
	var left []int = slices.Sorted(slices.Values(input[0]))
	var right []int = slices.Sorted(slices.Values(input[1]))
	result := 0
	for i := 0; i < len(left); i++ {
		d := left[i] - right[i]
		if d < 0 {
			result -= d
		} else {
			result += d
		}
	}
	return result
}

func frequencies(list []int) map[int]int {
	freq := make(map[int]int)
	for i := 0; i < len(list); i++ {
		val := list[i]
		if count, ok := freq[val]; ok {
			freq[val] = count + 1
		} else {
			freq[val] = 1
		}
	}
	return freq
}

func part2(input Input) int {
	right := frequencies(input[1])
	result := 0
	for i := 0; i < len(input[0]); i++ {
		left := input[0][i]
		result += left * right[left]
	}
	return result
}

func main() {
	b, err := os.ReadFile("../input/day_1.txt")
	if err != nil {
		panic(err)
	}

	input := parseInput(string(b))
	fmt.Println("part1:", part1(input))
	fmt.Println("part2:", part2(input))
}
