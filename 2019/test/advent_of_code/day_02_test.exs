defmodule AdventOfCode.Day02Test do
  use ExUnit.Case

  import AdventOfCode.Day02

  test "is_halt" do
    input = {99, 1, 2, 3, 4}
    assert is_halt(input, 0)
  end

  test "run_op" do
    input = {1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50}
    result = run_op(input, 0)
    assert result == {1, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50}
  end

  test "run_program" do
    input = {1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50}
    result = run_program(input, 0)
    assert result == {3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50}
  end

  test "small programs" do
    assert run_program({1, 0, 0, 0, 99}, 0) == {2, 0, 0, 0, 99}
    assert run_program({2, 3, 0, 3, 99}, 0) == {2, 3, 0, 6, 99}
    assert run_program({2, 4, 4, 5, 99, 0}, 0) == {2, 4, 4, 5, 99, 9801}
    assert run_program({1, 1, 1, 4, 99, 5, 6, 0, 99}, 0) == {30, 1, 1, 4, 2, 5, 6, 0, 99}
  end

  @tag :skip
  test "part2" do
    input = nil
    result = part2(input)

    assert result
  end
end
