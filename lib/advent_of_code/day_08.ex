defmodule AdventOfCode.Day08 do
  def frequencies(enumerable) do
    enumerable |> Enum.reduce(%{}, fn x, acc ->
      Map.update(acc, x, 1, &(&1 + 1))
    end)
  end

  def parse([input, width, height]) do
    input
    |> String.trim
    |> String.codepoints
    |> Enum.map(&String.to_integer/1)
    |> Enum.chunk_every(width * height)
  end

  def part1(args) do
    least_zeroes = parse(args)
    |> Enum.map(&frequencies/1)
    |> Enum.min_by(&Map.get(&1, 0, 0))

    Map.get(least_zeroes, 1, 0) * Map.get(least_zeroes, 2, 0)
  end

  def draw(image, width) do
    image
    |> Enum.map(fn
      0 -> " "
      1 -> "X"
      2 -> " "
    end)
    |> Enum.chunk_every(width)
    |> Enum.each(&IO.puts/1)
  end

  def part2([input, width, height]) do
    parse([input, width, height])
    |> Enum.reduce(fn layer, acc ->
      for {top, bottom} <- Enum.zip(acc, layer) do
        if top == 2, do: bottom, else: top
      end
    end)
    |> draw(width)
  end
end
