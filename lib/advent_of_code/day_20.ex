defmodule AdventOfCode.Day20 do
  import AdventOfCode.Utils
  alias Graph.Edge

  def parse(input) do
    input
    |> String.split("\n", trim: true)
    |> Stream.with_index()
    |> Stream.map(fn {line, y} ->
      line
      |> String.codepoints()
      |> Stream.with_index()
      |> Enum.map(fn {ch, x} ->
        {{x, y}, ch}
      end)
    end)
    |> Stream.concat()
    |> Map.new()
  end

  @doc """
  Scan for all reachable paths from vertex positioned at from.
  """
  def scan(map, vertices, from) do
    frontier = [from]
    visited = MapSet.new([from])
    scan(map, vertices, frontier, visited, 0, [])
  end

  def scan(_, _, [], _, _, edges), do: edges

  def scan(map, vertices, frontier, visited, steps, edges) do
    frontier =
      frontier
      |> Stream.map(&neighbors/1)
      |> Stream.concat()
      |> Stream.uniq()
      |> Stream.filter(&(Map.get(map, &1) == "."))
      |> Stream.reject(&MapSet.member?(visited, &1))
      |> Enum.to_list()

    visited =
      frontier
      |> MapSet.new()
      |> MapSet.union(visited)

    {hits, frontier} =
      frontier
      |> Enum.split_with(&Map.has_key?(vertices, &1))

    steps = steps + 1

    edges =
      hits
      |> Enum.map(&{Map.get(vertices, &1), steps + 1})
      |> Enum.reduce(edges, &[&1 | &2])

    scan(map, vertices, frontier, visited, steps, edges)
  end

  def is_inner?({x, y}, {{minx, miny}, {maxx, maxy}}) do
    cond do
      x == minx || x == maxx -> false
      y == miny || y == maxy -> false
      true -> true
    end
  end

  def find_vertex(map, {x, y}, level, ch, {dx, dy}) do
    next_ch = Map.get(map, {x + dx, y + dy})
    entrance = {x + dx + dx, y + dy + dy}

    if is_letter?(next_ch) and Map.get(map, entrance) == "." do
      name = if dx < 0 || dy < 0, do: next_ch <> ch, else: ch <> next_ch
      [{entrance, {name, level}}]
    else
      []
    end
  end

  def find_vertices(map) do
    dim = map_dimensions(map)

    map
    |> Stream.filter(fn {_, ch} -> is_letter?(ch) end)
    |> Enum.flat_map(fn {pos, ch} ->
      level = if is_inner?(pos, dim), do: 1, else: 0

      [{1, 0}, {-1, 0}, {0, 1}, {0, -1}]
      |> Enum.flat_map(&find_vertex(map, pos, level, ch, &1))
    end)
    |> Map.new()
  end

  def scan_edges(vertices, map) do
    vertices
    |> Enum.map(fn {pos, v} ->
      {v, scan(map, vertices, pos)}
    end)
  end

  def update_levels(nbh, fun) do
    Enum.map(nbh, fn {v1, edges} ->
      edges =
        Enum.map(edges, fn {v2, weight} ->
          {fun.(v2), weight}
        end)

      {fun.(v1), edges}
    end)
  end

  def drop_levels(nbh) do
    update_levels(nbh, fn {name, _} -> name end)
  end

  def to_graph(nbh) do
    Enum.reduce(nbh, Graph.new(), fn {from, edges}, acc ->
      Enum.reduce(edges, acc, fn {to, weight}, acc ->
        Graph.add_edge(acc, Edge.new(from, to, weight: weight))
      end)
    end)
  end

  def path_weight(path, graph) do
    path
    |> Stream.chunk_every(2, 1, :discard)
    |> Enum.map(fn [a, b] ->
      Graph.edges(graph, a, b)
      |> Enum.map(fn %Edge{:weight => w} -> w end)
      |> Enum.min()
    end)
    |> Enum.sum()
    |> dec()
  end

  def part1(input) do
    map = parse(input)

    graph =
      map
      |> find_vertices()
      |> scan_edges(map)
      |> drop_levels()
      |> to_graph()

    Graph.dijkstra(graph, "AA", "ZZ")
    |> path_weight(graph)
  end

  def part2(input) do
    map = parse(input)

    nbh =
      map
      |> find_vertices()
      |> scan_edges(map)

    graph =
      0..30
      |> Enum.map(fn i ->
        update_levels(nbh, fn {name, level} ->
          {name, level + i}
        end)
      end)
      |> Enum.concat()
      |> to_graph()

    Graph.dijkstra(graph, {"AA", 0}, {"ZZ", 0})
    |> path_weight(graph)
  end
end
