defmodule AdventOfCode.Day01 do
  def compute_fuel(mass) do
    max(0, div(mass, 3) - 2)
  end

  def part1(input) do
    input
    |> Enum.map(&compute_fuel/1)
    |> Enum.sum()
  end

  def compute_fuel_pt2(mass) do
    fuel = max(0, div(mass, 3) - 2)

    if fuel > 0 do
      fuel + compute_fuel_pt2(fuel)
    else
      fuel
    end
  end

  def part2(input) do
    input
    |> Enum.map(&compute_fuel_pt2/1)
    |> Enum.sum()
  end
end
