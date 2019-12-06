defmodule AdventOfCode.Day04 do
  def password?(number) do
    digits = Integer.digits(number)
    pairs = Enum.zip(digits, tl(digits))
    Enum.all?(pairs, fn({a, b}) -> a <= b end) and \
      Enum.any?(pairs, fn({a, b}) -> a == b end)
  end

  def part1([lower, upper]) do
    lower..upper |> Enum.count(&password?/1)
  end

  def has_group_of_two?(number) do
    Integer.digits(number)
    |> Enum.group_by(fn a -> a end)
    |> Map.values
    |> Enum.map(&length/1)
    |> Enum.any?(&(&1 == 2))
  end

  def part2([lower, upper]) do
    lower..upper |> Enum.count(fn num ->
      password?(num) and has_group_of_two?(num)
    end)
  end
end
