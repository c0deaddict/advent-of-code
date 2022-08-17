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

  @tag :skip
  test "part2" do
    input = nil
    result = part2(input)

    assert result
  end
end
