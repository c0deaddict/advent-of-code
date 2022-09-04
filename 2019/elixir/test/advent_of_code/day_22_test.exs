defmodule AdventOfCode.Day22Test do
  use ExUnit.Case

  import AdventOfCode.Day22

  test "deal with increment 3" do
    input = """
    deal with increment 3
    """
    result = shuffle(input, 10)
    assert result == [0,7,4,1,8,5,2,9,6,3]
  end

  test "part1 example1" do
    input = """
    deal with increment 7
    deal into new stack
    deal into new stack
    """
    result = shuffle(input, 10)
    assert result == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
  end

  test "part1 example2" do
    input = """
    cut 6
    deal with increment 7
    deal into new stack
    """
    result = shuffle(input, 10)
    assert result == [3,0,7,4,1,8,5,2,9,6]
  end

  test "part1 example3" do
    input = """
    deal with increment 7
    deal with increment 9
    cut -2
    """
    result = shuffle(input, 10)
    assert result == [6,3,0,7,4,1,8,5,2,9]
  end

  test "part1 example4" do
    input = """
    deal into new stack
    cut -2
    deal with increment 7
    cut 8
    cut -4
    deal with increment 7
    cut 3
    deal with increment 9
    deal with increment 3
    cut -1
    """
    result = shuffle(input, 10)
    assert result == [9,2,5,8,1,4,7,0,3,6]
  end

  test "deal with increment 3 and 4 is 2" do
    input1 = """
    deal with increment 3
    deal with increment 4
    """
    deal1 = shuffle(input1, 10)

    input2 = """
    deal with increment 2
    """
    deal2 = shuffle(input2, 10)

    assert deal1 == deal2
  end

  test "optimize" do
    input1 = """
    deal with increment 1
    cut 2
    deal with increment 1
    cut 3
    deal with increment 1
    cut 1
    """
    deal1 = shuffle(input1, 10)

    input2 = """
    deal with increment 1
    cut 6
    """
    deal2 = shuffle(input2, 10)

    assert deal1 == deal2

    assert optimize(parse(input1), 10) == {6, 1}
  end

  test "optimize 2" do
    input1 = """
    cut 2
    deal with increment 2
    cut 3
    deal with increment 2
    cut 1
    deal with increment 2
    """
    deal1 = shuffle(input1, 10)

    input2 = """
    deal with increment 8
    cut 0
    """
    deal2 = shuffle(input2, 10)

    assert deal1 == deal2

    assert optimize(parse(input1), 10) == {0, 8}
  end

  test "replace new stack with deal and cut" do
    input1 = """
    deal into new stack
    """
    deal1 = shuffle(input1, 10)

    input2 = """
    deal with increment -1
    cut 1
    """
    deal2 = shuffle(input2, 10)

    assert deal1 == deal2
  end

  test "optimize with new_stack" do
    input1 = """
    deal with increment 1
    deal into new stack
    cut 2
    deal into new stack
    deal with increment 1
    cut 3
    deal with increment 1
    cut 1
    deal into new stack
    """
    deal1 = shuffle(input1, 10)

    input2 = """
    deal with increment 9
    cut 9
    """
    deal2 = shuffle(input2, 10)

    assert deal1 == deal2

    assert optimize(parse(input1), 10) == {9, 9}
  end

  test "repetitions" do
    input1 = """
    deal with increment 13
    cut 53
    """
    n = 137
    IO.puts("")
    for i <- 1..100 do
      ops1 = repeat(parse(input1), n, i)
      ops2 = optimize(parse(String.duplicate(input1, i)), n)
      assert ops1 == ops2, "for #{i}: #{inspect(ops1)} != #{inspect(ops2)}"
    end
  end

  test "powmod" do
    assert powmod(2, 5, 13) == 6
  end

  test "divmod" do
    assert divmod(8, 3, 5) == 1
  end
end
