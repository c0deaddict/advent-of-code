defmodule AdventOfCode.Day24 do
  import AdventOfCode.Utils

  def parse(input) do
    input
    |> String.split("\n", trim: true)
    |> Stream.with_index()
    |> Stream.map(fn {line, y} ->
      line
      |> String.trim()
      |> String.codepoints()
      |> Stream.with_index()
      |> Enum.map(fn {ch, x} ->
        {{x, y}, ch == "#"}
      end)
    end)
    |> Stream.concat()
    |> Map.new()
  end

  def print_map(map) do
    {{minx, miny}, {maxx, maxy}} = map_dimensions(map)

    for y <- miny..maxy do
      minx..maxx
      |> Enum.map(fn x ->
        if Map.get(map, {x, y}), do: "#", else: "."
      end)
      |> IO.puts()
    end

    IO.puts("")
  end

  def iteration(map) do
    map
    |> Enum.map(fn {pos, bug} ->
      live_neighbors =
        neighbors(pos)
        |> Enum.filter(&Map.get(map, &1))
        |> Enum.count()

      new_bug =
        case {bug, live_neighbors} do
          {true, 1} -> true
          {false, 1} -> true
          {false, 2} -> true
          _ -> false
        end

      {pos, new_bug}
    end)
    |> Map.new()
  end

  def biodiversity_rating(map) do
    {{_, _}, {_, maxy}} = map_dimensions(map)

    map
    |> Enum.map(fn {{x, y}, bug} ->
      if bug, do: 2 ** (x + y * (maxy + 1)), else: 0
    end)
    |> Enum.sum()
  end

  def part1(input) do
    parse(input)
    |> Stream.iterate(&iteration/1)
    |> Enumerable.reduce({:cont, MapSet.new()}, fn map, set ->
      if MapSet.member?(set, map) do
        {:halt, map}
      else
        {:cont, MapSet.put(set, map)}
      end
    end)
    |> elem(1)
    |> biodiversity_rating()
  end

  def extend_if(list, condition, other) do
    if condition, do: list ++ other, else: list
  end

  def neighbors_part2({d, x, y}) do
    # Direct neighbors.
    [
      {d, x - 1, y},
      {d, x + 1, y},
      {d, x, y - 1},
      {d, x, y + 1}
    ]
    |> Enum.filter(fn {_, x, y} ->
      # Remove invalid coordinates and the center (it recurses down).
      x >= -2 and x <= 2 and y >= -2 and y <= 2 and not (x == 0 and y == 0)
    end)
    # Outside neighbors in upper depth.
    |> extend_if(y == -2, [{d + 1, 0, -1}])
    |> extend_if(y == 2, [{d + 1, 0, 1}])
    |> extend_if(x == -2, [{d + 1, -1, 0}])
    |> extend_if(x == 2, [{d + 1, 1, 0}])
    # Inside neighbors on lower depth.
    |> extend_if(x == 0 and y == -1, for(x <- -2..2, do: {d - 1, x, -2}))
    |> extend_if(x == 0 and y == 1, for(x <- -2..2, do: {d - 1, x, 2}))
    |> extend_if(x == -1 and y == 0, for(y <- -2..2, do: {d - 1, -2, y}))
    |> extend_if(x == 1 and y == 0, for(y <- -2..2, do: {d - 1, 2, y}))
  end

  def iteration_part2(map) do
    map
    |> Stream.map(fn pos ->
      (neighbors_part2(pos) ++ [pos])
      |> Enum.map(fn pos -> {pos, MapSet.member?(map, pos)} end)
    end)
    |> Stream.concat()
    |> Stream.uniq()
    |> Stream.map(fn {pos, bug} ->
      live_neighbors =
        neighbors_part2(pos)
        |> Enum.filter(&MapSet.member?(map, &1))
        |> Enum.count()

      new_bug =
        case {bug, live_neighbors} do
          {true, 1} -> true
          {false, 1} -> true
          {false, 2} -> true
          _ -> false
        end

      {pos, new_bug}
    end)
    |> Stream.filter(fn {_, bug} -> bug end)
    |> Enum.map(fn {pos, _} -> pos end)
    |> MapSet.new()
  end

  def part2_n(input, n) do
    parse(input)
    |> Enum.filter(fn {_, bug} -> bug end)
    |> Enum.map(fn {{x, y}, _} -> {1, x - 2, y - 2} end)
    |> MapSet.new()
    |> Stream.iterate(&iteration_part2/1)
    |> Stream.drop(n)
    |> Enum.take(1)
    |> hd
    |> MapSet.size()
  end

  def part2(input), do: part2_n(input, 200)
end
