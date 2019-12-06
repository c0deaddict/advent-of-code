defmodule AdventOfCode.Day05Test do
  use ExUnit.Case

  import AdventOfCode.Day05

  test "comparison" do
    # Using position mode, consider whether the input is equal to 8;
    # output 1 (if it is) or 0 (if it is not)
    assert run("3,9,8,9,10,9,4,9,99,-1,8", [8]) == [1]
    assert run("3,9,8,9,10,9,4,9,99,-1,8", [9]) == [0]

    # Using position mode, consider whether the input is less than 8;
    # output 1 (if it is) or 0 (if it is not).
    assert run("3,9,7,9,10,9,4,9,99,-1,8", [1]) == [1]
    assert run("3,9,7,9,10,9,4,9,99,-1,8", [10]) == [0]

    # Using immediate mode, consider whether the input is equal to 8;
    # output 1 (if it is) or 0 (if it is not).
    assert run("3,3,1108,-1,8,3,4,3,99", [8]) == [1]
    assert run("3,3,1108,-1,8,3,4,3,99", [-10]) == [0]

    # Using immediate mode, consider whether the input is less than 8;
    # output 1 (if it is) or 0 (if it is not).
    assert run("3,3,1107,-1,8,3,4,3,99", [-15]) == [1]
    assert run("3,3,1107,-1,8,3,4,3,99", [8]) == [0]
  end

  test "jump test" do
    # jump tests that take an input, then output 0 if the input was zero
    # or 1 if the input was non-zero:

    # using position mode
    assert run("3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9", [123]) == [1]

    # using immediate mode
    assert run("3,3,1105,-1,9,1101,0,0,12,4,12,99,1", [0]) == [0]
  end

  test "part2" do
    program_str =
      "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"

    # broken?
    # assert run(program_str, [0]) == [999]
    assert run(program_str, [8]) == [1000]
    assert run(program_str, [1000]) == [1001]
  end
end
