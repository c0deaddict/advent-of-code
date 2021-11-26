defmodule AdventOfCode.Day09Test do
  use ExUnit.Case

  import AdventOfCode.Day09

  test "part1 quine" do
    program_str = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"

    assert run(program_str, []) == [
             109,
             1,
             204,
             -1,
             1001,
             100,
             1,
             100,
             1008,
             100,
             16,
             101,
             1006,
             101,
             0,
             99
           ]
  end

  test "part1 16 digit number" do
    [result] = run("1102,34915192,34915192,7,4,7,99,0", [])
    assert result |> Integer.digits() |> length == 16
  end

  test "part1 large number" do
    assert run("104,1125899906842624,99", []) == [1_125_899_906_842_624]
  end

  @tag :skip
  test "part2" do
    input = nil
    result = part2(input)

    assert result
  end
end
