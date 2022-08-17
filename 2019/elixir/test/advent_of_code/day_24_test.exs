defmodule AdventOfCode.Day24Test do
  use ExUnit.Case

  import AdventOfCode.Day24

  test "part1" do
    input = """
      ....#
      #..#.
      #..##
      ..#..
      #....
    """
    result = part1(input)

    assert result == 2129920
  end

  test "part2" do
    input = """
      ....#
      #..#.
      #..##
      ..#..
      #....
    """
    result = part2_n(input, 10)

    assert result == 99
  end
end
