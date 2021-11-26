defmodule AdventOfCode.Day17Test do
  use ExUnit.Case

  import AdventOfCode.Day17

  test "part1" do
    input = """
    ..#..........
    ..#..........
    #######...###
    #.#...#...#.#
    #############
    ..#...#...#..
    ..#####...^..
    """

    result =
      input
      |> parse_image()
      |> calibrate()

    assert result == 76
  end

  test "find repetitions" do
    input = [1, 2, 3, 1, 2, 3, 4, 5, 2, 3, 1, 2, 3]
    assert find_repetitions(input, [1, 2, 3]) == [0, 3, 10]
  end

  test "sublists" do
    input = [1, 2, 3, 4]

    assert sublists(input) == [
             [1],
             [2],
             [3],
             [4],
             [1, 2],
             [2, 3],
             [3, 4],
             [1, 2, 3],
             [2, 3, 4],
             [1, 2, 3, 4]
           ]
  end

  test "permutations" do
    assert permutations([1, 2, 3, 4], 2) == [
             [1, 2],
             [1, 3],
             [1, 4],
             [2, 1],
             [2, 3],
             [2, 4],
             [3, 1],
             [3, 2],
             [3, 4],
             [4, 1],
             [4, 2],
             [4, 3]
           ]
  end

  test "permutations in order" do
    assert permutations_in_order([1, 2, 3, 4], 4) == [[1, 2, 3, 4]]

    assert permutations_in_order([1, 2, 3, 4], 2) == [
             [1, 2],
             [1, 3],
             [1, 4],
             [2, 3],
             [2, 4],
             [3, 4]
           ]
  end

  test "cover_all?" do
    assert cover_all?([{0, 2}, {2, 3}, {3, 9}], 10)
    assert not cover_all?([{0, 2}, {2, 3}, {3, 9}], 11)
    assert not cover_all?([{0, 2}, {2, 5}, {3, 10}], 10)
    assert not cover_all?([{0, 1}, {2, 3}, {3, 10}], 10)
  end
end
