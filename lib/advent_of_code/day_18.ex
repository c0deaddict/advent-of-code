defmodule AdventOfCode.Day18 do
  import AdventOfCode.Utils

  def parse(input) do
    input
    |> String.split("\n", trim: true)
    |> Stream.with_index()
    |> Stream.map(fn {line, y} ->
      line
      |> String.codepoints()
      |> Stream.with_index()
      |> Enum.map(fn {ch, x} ->
        tile =
          case ch do
            "#" ->
              :wall

            "." ->
              :empty

            "@" ->
              :entrance

            door_or_key ->
              if upcase?(door_or_key) do
                {:door, door_or_key}
              else
                {:key, door_or_key}
              end
          end

        {{x, y}, tile}
      end)
    end)
    |> Stream.concat()
    |> Map.new()
  end

  def neighbors({x, y}) do
    [
      {x, y - 1},
      {x, y + 1},
      {x - 1, y},
      {x + 1, y}
    ]
  end

  @doc """
  Scan for keys and doors that can be reached
  """
  def scan(map, pos, visited \\ MapSet.new(), steps \\ 0) do
    visited = MapSet.put(visited, pos)

    case Map.get(map, pos) do
      {type, name} ->
        [{type, name, pos, steps}]

      _ ->
        neighbors(pos)
        |> Enum.reject(&(Map.get(map, &1) == :wall))
        |> Enum.reject(&MapSet.member?(visited, &1))
        |> Enum.map(&scan(map, &1, visited, steps + 1))
        |> Enum.concat()
    end
  end

  def shortest_path(map, pos, steps \\ 0, path \\ []) do
    {keys, doors} =
      scan(map, pos)
      |> Enum.split_with(&(elem(&1, 0) == :key))

    case {keys, doors} do
      {[], []} ->
        IO.inspect({path, steps})
        steps

      {[], _} ->
        raise "locked in, doors left but no keys"

      _ ->
        # Branch taking a key, and unlocking the door.
        keys
        |> Enum.map(fn {:key, key, pos, steps_to_key} ->
          map = Map.put(map, pos, :empty)
          door_pos = find_key(map, {:door, String.upcase(key)})

          map =
          if door_pos != nil do
            Map.put(map, door_pos, :empty)
          else
            map
          end

          shortest_path(map, pos, steps + steps_to_key, [key | path])
        end)
        |> Enum.min()
    end
  end

  def draw_map(map) do
    keys = Map.keys(map)

    {{minx, _}, {maxx, _}} = Enum.min_max_by(keys, &elem(&1, 0))
    {{_, miny}, {_, maxy}} = Enum.min_max_by(keys, &elem(&1, 1))

    for y <- miny..maxy do
      line =
        minx..maxx
        |> Enum.map(fn x ->
          case Map.get(map, {x, y}) do
            :empty -> "."
            :wall -> "#"
            :entrance -> "@"
            {_, name} -> name
          end
        end)

      IO.puts(line)
    end
  end

  def part1(input) do
    map = parse(input)
    entrance = find_key(map, :entrance)
    shortest_path(map, entrance)
  end

  def part2(args) do
  end
end
