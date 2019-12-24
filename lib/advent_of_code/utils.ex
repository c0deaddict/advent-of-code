defmodule AdventOfCode.Utils do
  def transpose([]), do: []
  def transpose([[] | _]), do: []

  def transpose(a) do
    [Enum.map(a, &hd/1) | transpose(Enum.map(a, &tl/1))]
  end

  def gcd(a, 0), do: a
  def gcd(a, b), do: gcd(b, rem(a, b))

  def lcm(a, b), do: div(a * b, gcd(a, b))

  def find_cycle(stream) do
    stream
    |> Enum.reduce_while(Map.new(), fn i, acc ->
      case Map.get(acc, i) do
        nil ->
          {:cont, Map.put(acc, i, map_size(acc))}

        start ->
          {:halt, {start, map_size(acc)}}
      end
    end)
  end

  def repeat(stream, times) do
    [stream]
    |> Stream.cycle()
    |> Stream.take(times)
    |> Stream.concat()
  end

  def upcase?(str), do: String.upcase(str) == str

  def find_key(map, value) do
    Enum.find_value(map, fn {key, val} ->
      if val == value, do: key
    end)
  end

  def is_letter?(ch) do
    ch >= "A" and ch <= "Z"
  end

  def neighbors({x, y}) do
    [
      {x, y - 1},
      {x, y + 1},
      {x - 1, y},
      {x + 1, y}
    ]
  end

  def inc(i), do: i + 1
  def dec(i), do: i - 1

  def map_dimensions(map) do
    keys = Map.keys(map)

    {{minx, _}, {maxx, _}} = Enum.min_max_by(keys, &elem(&1, 0))
    {{_, miny}, {_, maxy}} = Enum.min_max_by(keys, &elem(&1, 1))

    {{minx, miny}, {maxx, maxy}}
  end
end
