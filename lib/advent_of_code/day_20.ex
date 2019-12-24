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
  Scan for all reachable paths from vertex v.
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

  def find_vertex(map, {x, y}, ch, {dx, dy}) do
    next_ch = Map.get(map, {x + dx, y + dy})
    entrance = {x + dx + dx, y + dy + dy}

    if is_letter?(next_ch) and Map.get(map, entrance) == "." do
      v = if dx < 0 || dy < 0, do: next_ch <> ch, else: ch <> next_ch
      [{entrance, v}]
    else
      []
    end
  end

  def find_vertices(map) do
    map
    |> Stream.filter(fn {_, ch} -> is_letter?(ch) end)
    |> Enum.flat_map(fn {pos, ch} ->
      [{1, 0}, {-1, 0}, {0, 1}, {0, -1}]
      |> Enum.flat_map(&find_vertex(map, pos, ch, &1))
    end)
    |> Map.new()
  end

  def to_graph(map) do
    vertices = find_vertices(map)

    vertices
    |> Enum.map(fn {pos, v} ->
      {v, scan(map, vertices, pos)}
    end)
    |> Enum.reduce(Graph.new(), fn {from, edges}, acc ->
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

  def shortest_path(graph) do
    Graph.dijkstra(graph, "AA", "ZZ")
  end

  def part1(input) do
    graph =
      input
      |> parse()
      |> to_graph()

    shortest_path(graph)
    |> path_weight(graph)
  end

  def part2(input) do
  end
end
