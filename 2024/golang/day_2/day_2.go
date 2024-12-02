package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Input = [][]int

func parseInput(input string) Input {
	var reports [][]int
	sc := bufio.NewScanner(strings.NewReader(input))
	for sc.Scan() {
		fields := strings.Fields(sc.Text())
		report := make([]int, len(fields))
		for i := 0; i < len(fields); i++ {
			v, err := strconv.Atoi(fields[i])
			if err != nil {
				panic(err)
			}
			report[i] = v
		}
		reports = append(reports, report)
	}
	return reports
}

func intAbs(i int) int {
	if i < 0 {
		return -i
	} else {
		return i
	}
}

func intSign(i int) bool {
	if i < 0 {
		return false
	} else {
		return true
	}
}

func isSafe(report []int) bool {
	sign := true
	for i := 0; i < len(report)-1; i++ {
		d := report[i] - report[i+1]
		if intAbs(d) < 1 || intAbs(d) > 3 {
			return false
		}
		if i == 0 {
			sign = intSign(d)
		} else if intSign(d) != sign {
			return false
		}
	}
	return true
}

func part1(input Input) int {
	count := 0
	for _, report := range input {
		if isSafe(report) {
			count += 1
		}
	}
	return count
}

func problemDampener(report []int) [][]int {
	result := make([][]int, len(report))
	for i := 0; i < len(report); i++ {
		other := make([]int, len(report)-1)
		j := 0
		for k := 0; k < len(report); k++ {
			if k != i {
				other[j] = report[k]
				j += 1
			}
		}
		result[i] = other
	}
	return result
}

func part2(input Input) int {
	count := 0
	for _, report := range input {
		if isSafe(report) {
			count += 1
		} else {
			for _, report := range problemDampener(report) {
				if isSafe(report) {
					count += 1
					break
				}
			}
		}
	}
	return count
}

func main() {
	b, err := os.ReadFile("../input/day_2.txt")
	if err != nil {
		panic(err)
	}

	input := parseInput(string(b))
	fmt.Println("part1:", part1(input))
	fmt.Println("part2:", part2(input))
}
