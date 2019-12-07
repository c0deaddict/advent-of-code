defmodule AdventOfCode.Day06 do
  def second([_, b]), do: b

  def parse(orbits_str) do
    orbits_str
    |> String.split("\n", trim: true)
    # split into [a, b] which means: b orbits around a
    |> Enum.map(&String.split(&1, ")", parts: 2))
  end

  def to_tree(orbits) do
    orbits
    # group by a
    |> Enum.group_by(&hd/1)
    # only keep list of b's as values
    |> Enum.map(fn {a, vals} ->
      {a, Enum.map(vals, &second/1)}
    end)
    |> Map.new()
  end

  def checksum(orbits_tree, key, depth) do
    depth +
      case orbits_tree[key] do
        nil ->
          0

        children ->
          children
          |> Enum.map(&checksum(orbits_tree, &1, depth + 1))
          |> Enum.sum()
      end
  end

  def part1(orbits_str) do
    orbits_tree = parse(orbits_str) |> to_tree
    checksum(orbits_tree, "COM", 0)
  end

  def parents_graph(orbits) do
    orbits
    |> Enum.map(&Enum.reverse/1)
    |> Enum.map(&List.to_tuple/1)
    |> Map.new()
  end

  def path(parents, key, acc \\ []) do
    acc = [key | acc]
    case parents[key] do
      nil -> acc
      p -> path(parents, p, acc)
    end
  end

  def part2(orbits_str) do
    parents = parse(orbits_str) |> parents_graph

    you_path = path(parents, "YOU")
    santa_path = path(parents, "SAN")

    # calculate the longest common prefix
    prefix_len = Enum.zip(you_path, santa_path)
    |> Enum.find_index(fn({a, b}) -> a != b end)

    (length(you_path) - prefix_len - 1) + (length(santa_path) - prefix_len - 1)
  end
end
