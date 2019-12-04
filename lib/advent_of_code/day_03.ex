defmodule AdventOfCode.Day03 do
  def parse_move("R" <> digits), do: {:right, String.to_integer(digits)}
  def parse_move("U" <> digits), do: {:up, String.to_integer(digits)}
  def parse_move("L" <> digits), do: {:left, String.to_integer(digits)}
  def parse_move("D" <> digits), do: {:down, String.to_integer(digits)}

  def parse_line(line) do
    String.split(line, ",")
    |> Enum.map(&parse_move/1)
  end

  def parse(input) do
    input
    |> String.split("\n", trim: true)
    |> Enum.map(&parse_line/1)
  end

  def in_dir(:right), do: {1, 0}
  def in_dir(:up), do: {0, 1}
  def in_dir(:left), do: {-1, 0}
  def in_dir(:down), do: {0, -1}

  def trace_line(line) do
    for({dir, dist} <- line, _ <- 1..dist, do: in_dir(dir))
    |> Enum.reduce([{0, 0}], fn {dx, dy}, res ->
      {x, y} = hd(res)
      pos = {x + dx, y + dy}
      [pos | res]
    end)
    |> Enum.reverse
  end

  def manhattan_distance({x, y}), do: abs(x) + abs(y)

  def intersect_traces(trace_1, trace_2) do
    MapSet.intersection(MapSet.new(trace_1), MapSet.new(trace_2))
  end

  def find_intersections(line_1, line_2) do
    trace_1 = line_1 |> trace_line
    trace_2 = line_2 |> trace_line

    intersect_traces(trace_1, trace_2)
    |> Enum.sort_by(&manhattan_distance/1)
  end

  def second([_, res | _]), do: res

  def find_closest_intersection(line_1, line_2) do
    find_intersections(line_1, line_2) |> second
  end

  def part1(input) do
    [line_1, line_2] = parse(input)

    find_closest_intersection(line_1, line_2)
    |> manhattan_distance
  end

  def trace_with_delay(trace) do
    trace
    |> Enum.with_index(0)
    |> Enum.reduce(%{}, fn {pos, delay}, acc ->
      Map.update(acc, pos, delay, &min(&1, delay))
    end)
  end

  def find_intersections_with_delay(line_1, line_2) do
    trace_1 = line_1 |> trace_line
    trace_2 = line_2 |> trace_line

    trace_1_with_delay = trace_with_delay(trace_1)
    trace_2_with_delay = trace_with_delay(trace_2)

    intersect_traces(trace_1, trace_2)
    |> Enum.map(fn pos ->
      delay_1 = trace_1_with_delay[pos]
      delay_2 = trace_2_with_delay[pos]
      {pos, delay_1 + delay_2}
    end)
    |> Enum.sort_by(&elem(&1, 1))
  end

  def find_min_signal_delay(line_1, line_2) do
    find_intersections_with_delay(line_1, line_2)
    |> second
    |> elem(1)
  end

  def part2(input) do
    [line_1, line_2] = parse(input)
    find_min_signal_delay(line_1, line_2)
  end
end
