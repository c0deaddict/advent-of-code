defmodule AdventOfCode.Day16Test do
  use ExUnit.Case

  import AdventOfCode.Day16

  test "part 1 test 1" do
    input = "12345678"

    result =
      input
      |> parse
      |> run(4)

    assert result = parse("01029498")
  end

  test "part 1 test 2" do
    input = "80871224585914546619083218645595"
    assert part1(input) == "24176176"
  end

  test "part 1 test 3" do
    input = "19617804207202209144916044189917"
    assert part1(input) == "73745418"
  end

  test "part 1 test 4" do
    input = "69317163492948606335995924319873"
    assert part1(input) == "52432133"
  end

  @tag :skip
  test "part2" do
    input = nil
    result = part2(input)

    assert result
  end
end
