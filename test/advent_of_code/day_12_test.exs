defmodule AdventOfCode.Day12Test do
  use ExUnit.Case

  import AdventOfCode.Day12

  test "part1 parse" do
    input = """
    <x=-1, y=0, z=2>
    <x=2, y=-10, z=-7>
    <x=4, y=-8, z=8>
    <x=3, y=5, z=-1>
    """

    assert parse(input) == [
             {{-1, 0, 2}, {0, 0, 0}},
             {{2, -10, -7}, {0, 0, 0}},
             {{4, -8, 8}, {0, 0, 0}},
             {{3, 5, -1}, {0, 0, 0}}
           ]
  end

  test "part1 test 1" do
    input = """
    <x=-1, y=0, z=2>
    <x=2, y=-10, z=-7>
    <x=4, y=-8, z=8>
    <x=3, y=5, z=-1>
    """

    result =
      parse(input)
      |> simulate
      |> Stream.take(10)
      |> Enum.to_list()

    assert Enum.at(result, 0) == [
             {{2, -1, 1}, {3, -1, -1}},
             {{3, -7, -4}, {1, 3, 3}},
             {{1, -7, 5}, {-3, 1, -3}},
             {{2, 2, 0}, {-1, -3, 1}}
           ]

    assert Enum.at(result, 1) == [
             {{5, -3, -1}, {3, -2, -2}},
             {{1, -2, 2}, {-2, 5, 6}},
             {{1, -4, -1}, {0, 3, -6}},
             {{1, -4, 2}, {-1, -6, 2}}
           ]

    assert Enum.at(result, 9) == [
             {{2, 1, -3}, {-3, -2, 1}},
             {{1, -8, 0}, {-1, 1, 3}},
             {{3, -6, 1}, {3, 2, -3}},
             {{2, 0, 4}, {1, -1, -1}}
           ]
  end

  test "part 1 test 1 total energy" do
    input = """
    <x=-1, y=0, z=2>
    <x=2, y=-10, z=-7>
    <x=4, y=-8, z=8>
    <x=3, y=5, z=-1>
    """

    result =
      parse(input)
      |> simulate_for(10)
      |> total_energy

    assert result == 179
  end

  test "part 1 test 2" do
    input = """
    <x=-8, y=-10, z=0>
    <x=5, y=5, z=10>
    <x=2, y=-7, z=3>
    <x=9, y=-8, z=-3>
    """

    result =
      parse(input)
      |> simulate_for(100)
      |> total_energy

    assert result == 1940
  end

  test "part2 test 1" do
    input = """
    <x=-1, y=0, z=2>
    <x=2, y=-10, z=-7>
    <x=4, y=-8, z=8>
    <x=3, y=5, z=-1>
    """

    assert part2(input) == 2772
  end

  test "part2 test large cycle" do
    input = """
    <x=-8, y=-10, z=0>
    <x=5, y=5, z=10>
    <x=2, y=-7, z=3>
    <x=9, y=-8, z=-3>
    """

    assert part2(input) == 4686774924
  end
end
