defmodule Mix.Tasks.D02.P1 do
  use Mix.Task

  import AdventOfCode.Day02

  @shortdoc "Day 02 Part 1"
  def run(args) do
    input =
      File.read!("../input/day_02.txt")
      |> String.trim()
      |> String.split(",")
      |> Enum.map(&String.to_integer/1)
      |> List.to_tuple()

    if Enum.member?(args, "-b"),
      do: Benchee.run(%{part_1: fn -> input |> part1() end}),
      else:
        input
        |> part1()
        |> IO.inspect(label: "Part 1 Results")
  end
end
