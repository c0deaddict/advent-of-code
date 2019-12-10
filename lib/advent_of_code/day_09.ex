defmodule AdventOfCode.Day09 do
  alias AdventOfCode.Day05, as: IntCode

  def run(program_str, input) do
    program_str
    |> IntCode.parse()
    |> IntCode.run(input)
  end

  def part1(program_str) do
    run(program_str, [1])
  end

  def part2(program_str) do
    run(program_str, [2])
  end
end
