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

  def key2door({:key, key}), do: {:door, String.upcase(key)}

  def is_key?({:key, _}), do: true
  def is_key?(_), do: false

  def is_door?({:door, _}), do: true
  def is_door?(_), do: false

  @doc """
  Scan for keys and doors that can be reached
  """
  def scan(map, from) do
    frontier = [from]
    visited = MapSet.new([from])
    scan(map, frontier, visited, 0, [])
  end

  def scan(_, [], _, _, edges), do: Map.new(edges)

  def scan(map, frontier, visited, steps, edges) do
    frontier =
      frontier
      |> Stream.map(&neighbors/1)
      |> Stream.concat()
      |> Stream.uniq()
      |> Stream.reject(&(Map.get(map, &1) == :wall))
      |> Stream.reject(&MapSet.member?(visited, &1))
      |> Enum.to_list()

    visited =
      frontier
      |> MapSet.new()
      |> MapSet.union(visited)

    {hits, frontier} =
      frontier
      |> Enum.split_with(&(Map.get(map, &1) != :empty))

    steps = steps + 1

    edges =
      hits
      |> Enum.map(&{Map.get(map, &1), steps})
      |> Enum.reduce(edges, &[&1 | &2])

    scan(map, frontier, visited, steps, edges)
  end

  def remove_vertex(graph, v) do
    remove_edges = Map.get(graph, v)

    graph
    |> Map.delete(v)
    |> Enum.map(fn {from, edges} ->
      new_edges =
        case Map.get(edges, v) do
          nil ->
            edges

          steps ->
            # Sorting descending on steps will resolve any conflicts in edges.
            # Map.new only includes the value of the _last_ {key, value} pair.
            remove_edges
            |> Map.delete(from)
            |> Enum.map(fn {to, v_steps} -> {to, steps + v_steps} end)
            |> Enum.concat(Map.delete(edges, v))
            |> Enum.sort_by(&elem(&1, 1), &>=/2)
            |> Map.new()
        end

      {from, new_edges}
    end)
    |> Map.new()
  end

  def shortest_path(graph) do
    keys_left =
      graph
      |> Map.keys()
      |> Enum.filter(&is_key?/1)

    shortest_path(graph, :entrance, keys_left, 0)
  end

  def shortest_path(_, _, [], steps), do: steps

  def shortest_path(graph, v, keys_left, steps) do
    v_edges = Map.get(graph, v)
    graph = remove_vertex(graph, v)

    v_edges
    |> Enum.filter(fn {to, _} -> Enum.member?(keys_left, to) end)
    |> Enum.map(fn {key, steps_to_key} ->
      door = key2door(key)
      # Unlock door by removing it.
      graph = remove_vertex(graph, door)
      keys_left = keys_left -- [key]
      shortest_path(graph, key, keys_left, steps + steps_to_key)
    end)
    |> Enum.min()
  end

  def draw_map(map) do
    {{minx, miny}, {maxx, maxy}} = map_dimensions(map)

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

  def filter_vertices(map) do
    map
    |> Enum.filter(fn
      {_, :entrance} -> true
      {_, {:key, _}} -> true
      {_, {:door, _}} -> true
      _ -> false
    end)
  end

  def part1(input) do
    map = parse(input)

    vertices =
      map
      |> filter_vertices()

    graph =
      vertices
      |> Enum.map(fn {pos, v} -> {v, scan(map, pos)} end)
      |> Map.new()

    shortest_path(graph)
  end

  def part2(args) do
  end
end
