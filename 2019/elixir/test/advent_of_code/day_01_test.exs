defmodule AdventOfCode.Day01Test do
  use ExUnit.Case

  import AdventOfCode.Day01

  test "compute fuel" do
    assert compute_fuel(12) == 2
    assert compute_fuel(14) == 2
    assert compute_fuel(1969) == 654
    assert compute_fuel(100_756) == 33583
  end

  @tag :skip
  test "part1" do
    input = nil
    result = part1(input)

    assert result
  end

  @tag :skip
  test "part2" do
    input = nil
    result = part2(input)

    assert result
  end
end
