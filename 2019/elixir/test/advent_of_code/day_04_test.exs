defmodule AdventOfCode.Day04Test do
  use ExUnit.Case

  import AdventOfCode.Day04

  test "part1" do
    assert password?(111_111)
    assert not password?(223_450)
    assert not password?(123_789)
  end

  test "part2" do
    assert has_group_of_two?(112_233)
    assert not has_group_of_two?(123_444)
    assert has_group_of_two?(111_122)
  end
end
