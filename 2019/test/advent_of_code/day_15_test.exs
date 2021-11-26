defmodule AdventOfCode.Day15Test do
  use ExUnit.Case

  import AdventOfCode.Day15

  test "part 2 example map" do
    input = """
     ##   
    #..## 
    #.#..#
    #.O.# 
     ###  
    """

    image = parse_image(input)

    oxygen =
      Enum.find_value(image, fn {pos, tile} ->
        if tile == :oxygen, do: pos
      end)

    assert oxygen == {2, 3}
    assert fill_oxygen(image, false, oxygen) == 4
  end
end
