defmodule AdventOfCode.Day19Test do
  use ExUnit.Case

  import AdventOfCode.Day19
  alias AdventOfCode.Day05, as: IntCode

  test "scan_stream" do
    input = File.read!("../input/day_19.txt")

    result =
      input
      |> IntCode.parse()
      |> scan_stream()
      |> Stream.take(50)
      |> image_from_stream()
      |> Enum.count(fn {{x, _}, value} -> x < 50 and value == 1 end)

    assert part1(input) == result
  end
end
