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

  def part2(_args) do
  end
end
