defmodule AdventOfCode.Day08Test do
  use ExUnit.Case

  import AdventOfCode.Day08

  test "frequencies" do
    assert frequencies([1, 1, 2, 3, 2, 3, 1]) == %{1 => 3, 2 => 2, 3 => 2}
  end
end
