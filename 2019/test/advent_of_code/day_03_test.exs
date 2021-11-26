defmodule AdventOfCode.Day03Test do
  use ExUnit.Case

  import AdventOfCode.Day03

  test "parse_move" do
    assert parse_move("R990") == {:right, 990}
    assert parse_move("U1") == {:up, 1}
    assert parse_move("L123456") == {:left, 123_456}
    assert parse_move("D0") == {:down, 0}
  end

  test "parse_line" do
    line = parse_line("R1,L2,U3,D4")
    assert line == [{:right, 1}, {:left, 2}, {:up, 3}, {:down, 4}]
  end

  test "part1 example 1" do
    input = """
    R8,U5,L5,D3
    U7,R6,D4,L4
    """

    assert part1(input) == 6
  end

  test "part1 example 2" do
    input = """
    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83
    """

    assert part1(input) == 159
  end

  test "part1 example 3" do
    input = """
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7
    """

    assert part1(input) == 135
  end

  test "part2 example 1" do
    input = """
    R8,U5,L5,D3
    U7,R6,D4,L4
    """

    assert part2(input) == 30
  end

  test "part2 example 2" do
    input = """
    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83
    """

    assert part2(input) == 610
  end

  test "part2 example 3" do
    input = """
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7
    """

    assert part2(input) == 410
  end
end
