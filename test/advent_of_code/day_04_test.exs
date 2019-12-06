defmodule AdventOfCode.Day04Test do
  use ExUnit.Case

  import AdventOfCode.Day04

  test "part1" do
    assert password?(111111)
    assert not password?(223450)
    assert not password?(123789)
  end

  test "part2" do
    assert has_group_of_two?(112233)
    assert not has_group_of_two?(123444)
    assert has_group_of_two?(111122)
  end
end
