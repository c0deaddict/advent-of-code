defmodule AdventOfCode.Day18Test do
  use ExUnit.Case

  import AdventOfCode.Day18

  test "part 1 example 1" do
    input = """
    #########
    #b.A.@.a#
    #########
    """

    assert part1(input) == 8
  end

  test "part 1 example 2" do
    input = """
    ########################
    #f.D.E.e.C.b.A.@.a.B.c.#
    ######################.#
    #d.....................#
    ########################
    """

    assert part1(input) == 86
  end

  test "part 1 example 3" do
    input = """
    ########################
    #...............b.C.D.f#
    #.######################
    #.....@.a.B.c.d.A.e.F.g#
    ########################
    """

    assert part1(input) == 132
  end

  test "part 1 example 4" do
    input = """
    #################
    #i.G..c...e..H.p#
    ########.########
    #j.A..b...f..D.o#
    ########@########
    #k.E..a...g..B.n#
    ########.########
    #l.F..d...h..C.m#
    #################
    """

    assert part1(input) == 136
  end

  test "part 1 example 5" do
    input = """
    ########################
    #@..............ac.GI.b#
    ###d#e#f################
    ###A#B#C################
    ###g#h#i################
    ########################
    """

    assert part1(input) == 81
  end
end
